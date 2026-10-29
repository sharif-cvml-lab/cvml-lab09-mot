from __future__ import annotations

import threading
import time
from pathlib import Path

import cv2
import numpy as np
from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtGui import QImage

from annotation import annotate_detections, annotate_tracks
from config import CAPTURE_HEIGHT, CAPTURE_WIDTH, DETECTION_COLOR, MODEL_PATH, TARGET_FPS, TrackingParameters
from detector import YoloDetector
from mot import Tracker
from tracking_types import Detection


def bgr_to_qimage(frame: np.ndarray) -> QImage:
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    height, width, channels = rgb.shape
    return QImage(rgb.data, width, height, channels * width, QImage.Format.Format_RGB888).copy()


class VideoThread(QThread):
    """Capture frames (camera, image or video), run YOLO and the student's tracker off the GUI thread."""

    # detection view, tracking view, detections, active tracks, lost tracks, IDs created, fps
    frame_ready = pyqtSignal(object, object, int, int, int, int, float)
    status_changed = pyqtSignal(str)
    processing_error = pyqtSignal(str)
    model_changed = pyqtSignal(str, object)  # model path, class names
    model_failed = pyqtSignal(str)

    def __init__(
        self,
        camera_index: int = 0,
        source_type: str = "camera",
        file_path: str = "",
        model_path: str | Path = MODEL_PATH,
        parent=None,
    ):
        super().__init__(parent)
        self._camera_index = camera_index
        self._source_type = source_type
        self._file_path = file_path
        self._parameters: TrackingParameters | None = None
        self._lock = threading.Lock()
        self._running = threading.Event()
        self._running.set()
        self._restart = threading.Event()
        self._reset_tracker = threading.Event()
        self._pending_model: Path | None = Path(model_path)
        self._paused = False
        self._last_status = ""
        self._last_error = ""

    def set_parameters(self, parameters: TrackingParameters) -> None:
        with self._lock:
            self._parameters = parameters

    def set_paused(self, paused: bool) -> None:
        with self._lock:
            self._paused = paused

    def set_model(self, model_path: str | Path) -> None:
        """Load another ONNX model (done inside the worker thread)."""
        with self._lock:
            self._pending_model = Path(model_path)

    def restart_source(self) -> None:
        self._restart.set()

    def reset_tracker(self) -> None:
        self._reset_tracker.set()

    def _snapshot(self) -> tuple[TrackingParameters | None, bool]:
        with self._lock:
            return self._parameters, self._paused

    def _emit_status(self, message: str) -> None:
        if message != self._last_status:
            self._last_status = message
            self.status_changed.emit(message)

    def _emit_error(self, message: str) -> None:
        if message != self._last_error:
            self._last_error = message
            self.processing_error.emit(message)

    def _open_source(self):
        """Return (capture, still_image). Exactly one of them is not None on success."""
        if self._source_type == "file":
            image = cv2.imread(self._file_path)
            if image is not None:
                return None, image
            cap = cv2.VideoCapture(self._file_path)
        else:
            cap = cv2.VideoCapture(self._camera_index)
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAPTURE_WIDTH)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAPTURE_HEIGHT)
        if not cap.isOpened():
            cap.release()
            return None, None
        return cap, None

    def _process(self, detector, tracker, frame, parameters, loop_started):
        detector.set_class_filter(parameters.class_filter)
        boxes, scores, class_ids = detector.detect(
            frame, parameters.confidence_threshold, parameters.detection_nms_threshold
        )
        detections = [Detection(b, float(s), int(c)) for b, s, c in zip(boxes, scores, class_ids)]

        # The GUI changes these hyperparameters live.
        tracker.iou_threshold = parameters.iou_threshold
        tracker.max_age = parameters.max_age
        tracker.min_hits = parameters.min_hits
        try:
            tracks = list(tracker.update(detections))
            self._emit_error("")
        except Exception as error:  # a bug in the student's code must not kill the app
            self._emit_error(f"{type(error).__name__}: {error}")
            tracks = []

        detection_view = annotate_detections(
            frame, boxes, scores, class_ids, DETECTION_COLOR, class_names=detector.class_names
        )
        tracking_view = annotate_tracks(
            frame, tracks, parameters.show_ids, parameters.show_trajectories,
            parameters.trajectory_length,
        )
        lost = sum(1 for t in tracks if t.missed > 0)
        elapsed = time.perf_counter() - loop_started
        fps = 1.0 / elapsed if elapsed > 0 else TARGET_FPS
        self.frame_ready.emit(
            bgr_to_qimage(detection_view), bgr_to_qimage(tracking_view),
            len(detections), len(tracks) - lost, lost, max(0, tracker.next_id - 1), fps,
        )

    def _take_pending_model(self):
        with self._lock:
            pending, self._pending_model = self._pending_model, None
        return pending

    def _load_model(self, path: Path, current):
        """Try to load a model. Returns the new detector, or the current one if loading fails."""
        try:
            detector = YoloDetector(path)
        except Exception as error:  # missing file, not a YOLO model, missing onnxruntime, ...
            self.model_failed.emit(f"{path.name}: {error}")
            self._emit_status(f"Model error: {error}")
            return current, False
        self.model_changed.emit(str(path), list(detector.class_names))
        self._emit_status(f"Model loaded: {path.name}")
        return detector, True

    def run(self) -> None:
        detector = None
        tracker = Tracker()
        cap = None
        still_image = None
        frame_period = 1.0 / TARGET_FPS
        try:
            while self._running.is_set():
                if self._restart.is_set():
                    self._restart.clear()
                    if cap is not None:
                        cap.release()
                    cap, still_image = None, None
                    tracker = Tracker()
                if self._reset_tracker.is_set():
                    self._reset_tracker.clear()
                    tracker = Tracker()

                pending_model = self._take_pending_model()
                if pending_model is not None:
                    detector, loaded = self._load_model(pending_model, detector)
                    if loaded:
                        tracker = Tracker()  # IDs of another model's classes make no sense
                parameters, paused = self._snapshot()
                if parameters is None or detector is None:
                    time.sleep(0.1)  # nothing to do yet (no parameters or no valid model)
                    continue

                if cap is None and still_image is None:
                    cap, still_image = self._open_source()
                    if cap is None and still_image is None:
                        self._emit_status("Source is unavailable. Retrying...")
                        time.sleep(1.0)
                        continue
                    self._emit_status("Source connected")

                if paused:
                    self._emit_status("Paused")
                    time.sleep(frame_period)
                    continue
                if self._last_status == "Paused":
                    self._emit_status("Source connected")

                loop_started = time.perf_counter()
                if still_image is not None:
                    frame = still_image
                else:
                    ret, frame = cap.read()
                    if not ret:
                        if self._source_type == "file":  # video file: loop, IDs start again
                            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                            tracker = Tracker()
                            ret, frame = cap.read()
                        if not ret:
                            self._emit_status("Frame read failed. Reconnecting...")
                            cap.release()
                            cap = None
                            time.sleep(0.25)
                            continue

                self._process(detector, tracker, frame, parameters, loop_started)
                elapsed = time.perf_counter() - loop_started
                time.sleep(max(0.0, frame_period - elapsed))
        finally:
            if cap is not None:
                cap.release()
            self._emit_status("Source stopped")

    def stop(self) -> None:
        self._running.clear()
        self.wait()
