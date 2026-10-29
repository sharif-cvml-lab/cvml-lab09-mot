from __future__ import annotations

from pathlib import Path

from PyQt6.QtCore import QSettings, QSize, Qt
from PyQt6.QtGui import QImage, QKeySequence, QPixmap, QShortcut
from PyQt6.QtWidgets import (
    QApplication,
    QCheckBox,
    QFileDialog,
    QFrame,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QSlider,
    QStyle,
    QSpinBox,
    QSplitter,
    QVBoxLayout,
    QWidget,
)

from config import (
    APP_NAME,
    COCO_CLASSES,
    DEFAULT_ASSOCIATION_IOU_PERCENT,
    DEFAULT_CAMERA_INDEX,
    DEFAULT_CONFIDENCE_PERCENT,
    DEFAULT_DETECTION_NMS_PERCENT,
    DEFAULT_MAX_AGE,
    DEFAULT_MIN_HITS,
    DEFAULT_SETTINGS_MESSAGE,
    DEFAULT_SHOW_IDS,
    DEFAULT_SHOW_TRAJECTORIES,
    DEFAULT_THEME,
    DEFAULT_TRAJECTORY_LENGTH,
    FILE_FILTER,
    MODEL_PATH,
    ORGANIZATION_NAME,
    TrackingParameters,
)
from video_thread import VideoThread


DARK_STYLE = """
QMainWindow, QWidget {
    background: #11151b;
    color: #e7ebf0;
    font-family: "Segoe UI", Arial, sans-serif;
    font-size: 13px;
}
QFrame#Header, QFrame#SidebarCard, QFrame#VideoCard, QFrame#StatusBar {
    background: #171c23;
    border: 1px solid #28303a;
    border-radius: 12px;
}
QFrame#VideoCanvas {
    background: #0a0d11;
    border: 1px solid #303945;
    border-radius: 10px;
}
QLabel#Title { font-size: 22px; font-weight: 700; }
QLabel#Subtitle, QLabel#Muted { color: #8e98a6; }
QLabel#PanelTitle { font-size: 14px; font-weight: 700; }
QLabel#Metric { color: #9aa6b4; font-size: 12px; }
QLabel#MetricValue { font-size: 15px; font-weight: 700; }
QLabel#ValueChip {
    background: #202833;
    border: 1px solid #364250;
    border-radius: 6px;
    padding: 2px 8px;
    min-width: 42px;
}
QPushButton {
    background: #212833;
    color: #eef2f6;
    border: 1px solid #35404d;
    border-radius: 8px;
    padding: 8px 12px;
}
QPushButton:hover { background: #2a3441; border-color: #4e6175; }
QPushButton:pressed { background: #18202a; }
QPushButton#accent { background: #3a7d67; border-color: #4c9b80; font-weight: 700; }
QPushButton#accent:hover { background: #479276; }
QPushButton#danger { background: #322126; border-color: #5d333d; }
QSpinBox {
    background: #1a2028;
    border: 1px solid #35404d;
    border-radius: 7px;
    padding: 6px;
}
QSlider::groove:horizontal { height: 5px; background: #2b333d; border-radius: 3px; }
QSlider::sub-page:horizontal { background: #4d9d80; border-radius: 3px; }
QSlider::handle:horizontal {
    background: #80c6ab;
    border: 1px solid #9ad9c0;
    width: 14px;
    margin: -5px 0;
    border-radius: 7px;
}
QGroupBox {
    border: 1px solid #28303a;
    border-radius: 10px;
    margin-top: 12px;
    padding-top: 12px;
    font-weight: 700;
}
QGroupBox::title { left: 12px; padding: 0 6px; }
QScrollArea { border: none; background: transparent; }
QScrollBar:vertical { width: 10px; background: transparent; }
QScrollBar::handle:vertical { background: #313b47; border-radius: 5px; min-height: 30px; }
QLabel#Error { color: #ff7b7b; font-weight: 700; }
QCheckBox { spacing: 8px; }
QListWidget, QComboBox {
    background: #1a2028;
    border: 1px solid #35404d;
    border-radius: 7px;
    padding: 4px;
}
"""

LIGHT_STYLE = """
QMainWindow, QWidget {
    background: #eef1f5;
    color: #1d252d;
    font-family: "Segoe UI", Arial, sans-serif;
    font-size: 13px;
}
QFrame#Header, QFrame#SidebarCard, QFrame#VideoCard, QFrame#StatusBar {
    background: #ffffff;
    border: 1px solid #d3dae2;
    border-radius: 12px;
}
QFrame#VideoCanvas {
    background: #dfe5ec;
    border: 1px solid #c4ccd6;
    border-radius: 10px;
}
QLabel#Title { font-size: 22px; font-weight: 700; }
QLabel#Subtitle, QLabel#Muted { color: #5f6b78; }
QLabel#PanelTitle { font-size: 14px; font-weight: 700; }
QLabel#Metric { color: #5f6b78; font-size: 12px; }
QLabel#MetricValue { font-size: 15px; font-weight: 700; }
QLabel#Error { color: #c0392b; font-weight: 700; }
QLabel#ValueChip {
    background: #e8edf2;
    border: 1px solid #c4ccd6;
    border-radius: 6px;
    padding: 2px 8px;
    min-width: 42px;
}
QPushButton {
    background: #f7f9fb;
    color: #1d252d;
    border: 1px solid #c4ccd6;
    border-radius: 8px;
    padding: 8px 12px;
}
QPushButton:hover { background: #e8eef4; border-color: #8fa3b5; }
QPushButton:pressed { background: #dbe3ea; }
QPushButton#accent { background: #3a7d67; color: #ffffff; border-color: #4c9b80; font-weight: 700; }
QPushButton#accent:hover { background: #479276; }
QPushButton#danger { background: #f8e3e6; border-color: #e0b4bc; }
QSpinBox, QListWidget, QComboBox {
    background: #ffffff;
    border: 1px solid #c4ccd6;
    border-radius: 7px;
    padding: 6px;
}
QSlider::groove:horizontal { height: 5px; background: #cdd5de; border-radius: 3px; }
QSlider::sub-page:horizontal { background: #4d9d80; border-radius: 3px; }
QSlider::handle:horizontal {
    background: #3a7d67;
    border: 1px solid #2c614f;
    width: 14px;
    margin: -5px 0;
    border-radius: 7px;
}
QGroupBox {
    border: 1px solid #d3dae2;
    border-radius: 10px;
    margin-top: 12px;
    padding-top: 12px;
    font-weight: 700;
}
QGroupBox::title { left: 12px; padding: 0 6px; }
QScrollArea { border: none; background: transparent; }
QScrollBar:vertical { width: 10px; background: transparent; }
QScrollBar::handle:vertical { background: #bcc6d1; border-radius: 5px; min-height: 30px; }
"""


class VideoLabel(QLabel):
    """Scalable image view that preserves the source aspect ratio."""

    def __init__(self):
        super().__init__()
        self._pixmap = QPixmap()
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setMinimumSize(260, 190)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

    def set_frame(self, image: QImage) -> None:
        self._pixmap = QPixmap.fromImage(image)
        self._refresh_pixmap()

    def clear_frame(self) -> None:
        self._pixmap = QPixmap()
        self.clear()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._refresh_pixmap()

    def _refresh_pixmap(self) -> None:
        if self._pixmap.isNull():
            return
        self.setPixmap(
            self._pixmap.scaled(
                self.size(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
        )


class ValueSlider(QWidget):
    def __init__(self, title: str, minimum: int, maximum: int, value: int, parent=None):
        super().__init__(parent)
        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setRange(minimum, maximum)
        self.slider.setValue(value)
        self.title_label = QLabel(title)
        self.title_label.setMinimumWidth(120)
        self.value_label = QLabel(str(value))
        self.value_label.setObjectName("ValueChip")
        self.value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 2, 0, 2)
        layout.setSpacing(8)
        layout.addWidget(self.title_label)
        layout.addWidget(self.slider, 1)
        layout.addWidget(self.value_label)
        self.slider.valueChanged.connect(self._on_value_changed)

    def _on_value_changed(self, value: int) -> None:
        self.value_label.setText(str(value))

    def value(self) -> int:
        return self.slider.value()

    def set_value(self, value: int) -> None:
        self.slider.setValue(value)


class AppWindow(QMainWindow):
    """Main interactive UI for Lab 09."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle(APP_NAME)
        self.setMinimumSize(QSize(1120, 740))
        self.resize(1400, 900)

        self.settings = QSettings(ORGANIZATION_NAME, APP_NAME)
        self.video_thread: VideoThread | None = None
        self.selected_file = ""
        self.source_type = "camera"
        self.theme = DEFAULT_THEME
        self.model_path = str(MODEL_PATH)  # the model that is (or will be) loaded
        self._closing = False
        self._restoring = False

        self._build_ui()
        self._restore_settings()
        self._build_shortcuts()
        self._apply_theme()
        self._start_video_thread()

    def _build_ui(self) -> None:
        central = QWidget()
        root = QVBoxLayout(central)
        root.setContentsMargins(14, 14, 14, 12)
        root.setSpacing(12)

        header = QFrame()
        header.setObjectName("Header")
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(18, 14, 18, 14)
        title_box = QVBoxLayout()
        title = QLabel("Multi-Object Tracking Playground")
        title.setObjectName("Title")
        subtitle = QLabel("Interactive YOLO detection and IoU-based multi-object tracking")
        subtitle.setObjectName("Subtitle")
        title_box.addWidget(title)
        title_box.addWidget(subtitle)
        header_layout.addLayout(title_box, 1)
        self.theme_button = QPushButton("Light Mode")
        self.theme_button.clicked.connect(self._toggle_theme)
        header_layout.addWidget(self.theme_button)
        self.reset_button = QPushButton("Reset")
        self.reset_button.setObjectName("danger")
        self.reset_button.clicked.connect(self._reset_defaults)
        header_layout.addWidget(self.reset_button)
        root.addWidget(header)

        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setChildrenCollapsible(False)

        video_side = QWidget()
        video_layout = QVBoxLayout(video_side)
        video_layout.setContentsMargins(0, 0, 0, 0)
        video_grid = QGridLayout()
        video_grid.setSpacing(10)
        self.detection_panel = self._create_video_card("Detection View")
        self.tracking_panel = self._create_video_card("Tracking View")
        video_grid.addWidget(self.detection_panel, 0, 0)
        video_grid.addWidget(self.tracking_panel, 0, 1)
        for column in range(2):
            video_grid.setColumnStretch(column, 1)
        video_layout.addLayout(video_grid, 1)

        status = QFrame()
        status.setObjectName("StatusBar")
        status_layout = QHBoxLayout(status)
        status_layout.setContentsMargins(14, 8, 14, 8)
        self.status_label = QLabel("Starting source...")
        self.status_label.setObjectName("Muted")
        self.error_label = QLabel("")
        self.error_label.setObjectName("Error")
        self.settings_label = QLabel(DEFAULT_SETTINGS_MESSAGE)
        self.settings_label.setObjectName("MetricValue")
        self.fps_label = QLabel("FPS: --")
        self.fps_label.setObjectName("MetricValue")
        status_layout.addWidget(self.status_label, 1)
        status_layout.addWidget(self.error_label)
        status_layout.addSpacing(18)
        status_layout.addWidget(self.settings_label)
        status_layout.addSpacing(18)
        status_layout.addWidget(self.fps_label)
        video_layout.addWidget(status)

        splitter.addWidget(video_side)
        splitter.addWidget(self._build_sidebar())
        splitter.setSizes([1020, 380])
        root.addWidget(splitter, 1)
        self.setCentralWidget(central)

    def _create_video_card(self, title: str) -> QFrame:
        card = QFrame()
        card.setObjectName("VideoCard")
        layout = QVBoxLayout(card)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(8)
        title_label = QLabel(title)
        title_label.setObjectName("PanelTitle")
        layout.addWidget(title_label)
        canvas = QFrame()
        canvas.setObjectName("VideoCanvas")
        canvas_layout = QVBoxLayout(canvas)
        canvas_layout.setContentsMargins(0, 0, 0, 0)
        image = VideoLabel()
        image.setText("Waiting for source...")
        canvas_layout.addWidget(image)
        layout.addWidget(canvas, 1)
        card.image = image
        return card

    def _build_sidebar(self) -> QWidget:
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setContentsMargins(4, 0, 4, 0)
        layout.setSpacing(10)

        model_box = QGroupBox("Model")
        model_layout = QHBoxLayout(model_box)
        self.model_label = QLabel(Path(self.model_path).name)
        self.model_label.setObjectName("MetricValue")
        self.model_label.setToolTip(self.model_path)
        self.model_label.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Preferred)
        self.model_button = QPushButton()
        self.model_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_DirOpenIcon))
        self.model_button.setToolTip("Browse for an ONNX model on this computer")
        self.model_button.setFixedWidth(46)
        self.model_button.clicked.connect(self._browse_model)
        model_layout.addWidget(self.model_label, 1)
        model_layout.addWidget(self.model_button)
        layout.addWidget(model_box)

        source_box = QGroupBox("Input Source")
        source_layout = QVBoxLayout(source_box)
        camera_row = QHBoxLayout()
        camera_row.addWidget(QLabel("Camera index"))
        self.camera_spin = QSpinBox()
        self.camera_spin.setRange(0, 9)
        self.camera_spin.valueChanged.connect(self._camera_index_changed)
        camera_row.addWidget(self.camera_spin)
        source_layout.addLayout(camera_row)

        camera_buttons = QHBoxLayout()
        self.webcam_button = QPushButton("Webcam")
        self.webcam_button.clicked.connect(self._use_webcam)
        self.browse_button = QPushButton("Browse")
        self.browse_button.clicked.connect(self._browse_file)
        self.upload_button = QPushButton("Upload")
        self.upload_button.setObjectName("accent")
        self.upload_button.setEnabled(False)
        self.upload_button.clicked.connect(self._upload_selected_file)
        camera_buttons.addWidget(self.webcam_button)
        camera_buttons.addWidget(self.browse_button)
        camera_buttons.addWidget(self.upload_button)
        source_layout.addLayout(camera_buttons)

        self.file_label = QLabel("No offline video selected")
        self.file_label.setObjectName("Muted")
        self.file_label.setWordWrap(True)
        source_layout.addWidget(self.file_label)

        action_row = QHBoxLayout()
        self.pause_button = QPushButton("Pause")
        self.pause_button.clicked.connect(self._toggle_pause)
        self.restart_button = QPushButton("Restart")
        self.restart_button.clicked.connect(self._restart_source)
        action_row.addWidget(self.pause_button)
        action_row.addWidget(self.restart_button)
        source_layout.addLayout(action_row)
        layout.addWidget(source_box)

        detector_box = QGroupBox("Detector Configuration")
        detector_layout = QVBoxLayout(detector_box)
        self.confidence_slider = ValueSlider("Confidence ×100", 5, 95, DEFAULT_CONFIDENCE_PERCENT)
        self.detection_nms_slider = ValueSlider("Detector NMS ×100", 5, 95, DEFAULT_DETECTION_NMS_PERCENT)
        detector_layout.addWidget(self.confidence_slider)
        detector_layout.addWidget(self.detection_nms_slider)
        layout.addWidget(detector_box)

        tracker_box = QGroupBox("Tracker Configuration")
        tracker_layout = QVBoxLayout(tracker_box)
        self.association_slider = ValueSlider("Association IoU ×100", 5, 95, DEFAULT_ASSOCIATION_IOU_PERCENT)
        self.max_age_slider = ValueSlider("Max missed frames", 0, 60, DEFAULT_MAX_AGE)
        self.min_hits_slider = ValueSlider("Min hits (track age)", 1, 10, DEFAULT_MIN_HITS)
        self.trajectory_slider = ValueSlider("Trajectory length", 5, 100, DEFAULT_TRAJECTORY_LENGTH)
        for control in (self.association_slider, self.max_age_slider, self.min_hits_slider, self.trajectory_slider):
            tracker_layout.addWidget(control)
        self.ids_check = QCheckBox("Show IDs")
        self.trajectory_check = QCheckBox("Show trajectories")
        tracker_layout.addWidget(self.ids_check)
        tracker_layout.addWidget(self.trajectory_check)
        self.reset_tracker_button = QPushButton("Reset Tracker")
        self.reset_tracker_button.clicked.connect(self._reset_tracker)
        tracker_layout.addWidget(self.reset_tracker_button)
        layout.addWidget(tracker_box)

        class_box = QGroupBox("Class Filter")
        class_layout = QVBoxLayout(class_box)
        self.class_list = QListWidget()
        self.class_list.setMinimumHeight(150)
        for name in COCO_CLASSES:
            item = QListWidgetItem(name)
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            item.setCheckState(Qt.CheckState.Checked)
            self.class_list.addItem(item)
        class_layout.addWidget(self.class_list)
        class_buttons = QHBoxLayout()
        self.all_classes_button = QPushButton("All")
        self.all_classes_button.clicked.connect(lambda: self._set_all_classes(True))
        self.no_classes_button = QPushButton("None")
        self.no_classes_button.clicked.connect(lambda: self._set_all_classes(False))
        class_buttons.addWidget(self.all_classes_button)
        class_buttons.addWidget(self.no_classes_button)
        class_layout.addLayout(class_buttons)
        layout.addWidget(class_box)

        stats_box = QGroupBox("Statistics")
        stats_layout = QGridLayout(stats_box)
        self.metric_values: dict[str, QLabel] = {}
        for row, name in enumerate(("Detections", "Active tracks", "Lost tracks", "IDs created", "FPS")):
            label = QLabel(name)
            label.setObjectName("Metric")
            value = QLabel("--")
            value.setObjectName("MetricValue")
            stats_layout.addWidget(label, row, 0)
            stats_layout.addWidget(value, row, 1)
            self.metric_values[name] = value
        layout.addWidget(stats_box)
        layout.addStretch(1)

        for control in (
            self.confidence_slider, self.detection_nms_slider, self.association_slider,
            self.max_age_slider, self.min_hits_slider, self.trajectory_slider,
        ):
            control.slider.valueChanged.connect(self._parameters_changed)
        for check in (self.ids_check, self.trajectory_check):
            check.toggled.connect(self._parameters_changed)
        self.class_list.itemChanged.connect(self._parameters_changed)

        scroll.setWidget(content)
        return scroll

    def _build_shortcuts(self) -> None:
        QShortcut(QKeySequence("Space"), self, activated=self._toggle_pause)
        QShortcut(QKeySequence("F11"), self, activated=self._toggle_fullscreen)
        QShortcut(QKeySequence("R"), self, activated=self._reset_defaults)
        QShortcut(QKeySequence("Q"), self, activated=self.close)

    def _selected_classes(self) -> tuple[int, ...] | None:
        selected = tuple(
            index
            for index in range(self.class_list.count())
            if self.class_list.item(index).checkState() == Qt.CheckState.Checked
        )
        return None if len(selected) == self.class_list.count() else selected

    def _current_parameters(self) -> TrackingParameters:
        return TrackingParameters(
            confidence_threshold=self.confidence_slider.value() / 100.0,
            detection_nms_threshold=self.detection_nms_slider.value() / 100.0,
            iou_threshold=self.association_slider.value() / 100.0,
            max_age=self.max_age_slider.value(),
            min_hits=self.min_hits_slider.value(),
            trajectory_length=self.trajectory_slider.value(),
            class_filter=self._selected_classes(),
            show_ids=self.ids_check.isChecked(),
            show_trajectories=self.trajectory_check.isChecked(),
        )

    def _start_video_thread(self) -> None:
        self._stop_video_thread()
        self.video_thread = VideoThread(
            camera_index=self.camera_spin.value(),
            source_type=self.source_type,
            file_path=self.selected_file,
            model_path=self.model_path,
            parent=self,
        )
        self.video_thread.set_parameters(self._current_parameters())
        self.video_thread.model_changed.connect(self._on_model_changed)
        self.video_thread.model_failed.connect(self._on_model_failed)
        self.video_thread.frame_ready.connect(self._update_frames)
        self.video_thread.status_changed.connect(self.status_label.setText)
        self.video_thread.processing_error.connect(self._show_error)
        self.video_thread.start()
        self.pause_button.setText("Pause")
        self.status_label.setText("Starting source...")

    def _stop_video_thread(self) -> None:
        if self.video_thread is not None:
            self.video_thread.stop()
            self.video_thread.deleteLater()
            self.video_thread = None

    def _update_frames(
        self, qt_detection, qt_tracking, detections: int, active: int, lost: int, ids_created: int, fps: float
    ) -> None:
        self.detection_panel.image.set_frame(qt_detection)
        self.tracking_panel.image.set_frame(qt_tracking)
        self.metric_values["Detections"].setText(str(detections))
        self.metric_values["Active tracks"].setText(str(active))
        self.metric_values["Lost tracks"].setText(str(lost))
        self.metric_values["IDs created"].setText(str(ids_created))
        self.metric_values["FPS"].setText(f"{fps:.1f}")
        self.fps_label.setText(f"FPS: {fps:.1f}")

    def _show_error(self, message: str) -> None:
        self.error_label.setText(f"Tracker.update error: {message}" if message else "")

    def _parameters_changed(self, *_args) -> None:
        if self._restoring:
            return
        self._save_settings()
        if self.video_thread is not None:
            self.video_thread.set_parameters(self._current_parameters())

    def _set_all_classes(self, checked: bool) -> None:
        state = Qt.CheckState.Checked if checked else Qt.CheckState.Unchecked
        self.class_list.blockSignals(True)
        for index in range(self.class_list.count()):
            self.class_list.item(index).setCheckState(state)
        self.class_list.blockSignals(False)
        self._parameters_changed()

    # ---- model selection
    def _browse_model(self) -> None:
        start_dir = str(Path(self.model_path).parent) if Path(self.model_path).exists() else ""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select ONNX model", start_dir, "ONNX models (*.onnx);;All Files (*)"
        )
        if file_path and self.video_thread is not None:
            self.status_label.setText(f"Loading model {Path(file_path).name}...")
            self.video_thread.set_model(file_path)

    def _on_model_changed(self, path: str, class_names) -> None:
        """Called after the worker thread loaded a model successfully (the tracker restarts)."""
        self.model_path = path
        self.model_label.setText(Path(path).name)
        self.model_label.setToolTip(path)
        self.error_label.setText("")
        self._set_class_names(list(class_names))
        self._save_settings()

    def _on_model_failed(self, message: str) -> None:
        """The previous model stays active when a new one cannot be loaded."""
        self.error_label.setText(f"Model error: {message}")

    def _set_class_names(self, names: list[str]) -> None:
        current = [self.class_list.item(i).text() for i in range(self.class_list.count())]
        if names == current:
            return
        self.class_list.blockSignals(True)
        self.class_list.clear()
        for name in names:
            item = QListWidgetItem(name)
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            item.setCheckState(Qt.CheckState.Checked)
            self.class_list.addItem(item)
        self.class_list.blockSignals(False)
        self._parameters_changed()

    def _reset_tracker(self) -> None:
        if self.video_thread is not None:
            self.video_thread.reset_tracker()
            self.status_label.setText("Tracker reset: IDs start again from 1.")

    def _use_webcam(self) -> None:
        self.source_type = "camera"
        self._save_settings()
        self._start_video_thread()

    def _camera_index_changed(self, _value: int) -> None:
        self._save_settings()
        if self.source_type == "camera" and not self._closing and self.video_thread is not None:
            self._start_video_thread()

    def _browse_file(self) -> None:
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Video", "", FILE_FILTER)
        if not file_path:
            return
        self.selected_file = file_path
        self.file_label.setText(f"Selected: {Path(file_path).name}")
        self.upload_button.setEnabled(True)
        self.status_label.setText("File selected. Click Upload to process it.")

    def _upload_selected_file(self) -> None:
        if not self.selected_file:
            self.status_label.setText("No file selected. Click Browse first.")
            return
        self.source_type = "file"
        self._save_settings()
        self._start_video_thread()

    def _toggle_pause(self) -> None:
        if self.video_thread is None:
            return
        paused = self.pause_button.text() == "Pause"
        self.video_thread.set_paused(paused)
        self.pause_button.setText("Resume" if paused else "Pause")

    def _restart_source(self) -> None:
        if self.video_thread is not None:
            self.video_thread.restart_source()
            self.pause_button.setText("Pause")
            self.video_thread.set_paused(False)
            self.status_label.setText("Restarting source...")
        else:
            self._start_video_thread()

    def _toggle_fullscreen(self) -> None:
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

    def _toggle_theme(self) -> None:
        self.theme = "light" if self.theme == "dark" else "dark"
        self._apply_theme()
        self._save_settings()

    def _apply_theme(self) -> None:
        self.setStyleSheet(DARK_STYLE if self.theme == "dark" else LIGHT_STYLE)
        self.theme_button.setText("Light Mode" if self.theme == "dark" else "Dark Mode")

    def _reset_defaults(self) -> None:
        self._restoring = True
        self.camera_spin.blockSignals(True)
        self.camera_spin.setValue(DEFAULT_CAMERA_INDEX)
        self.camera_spin.blockSignals(False)
        self.confidence_slider.set_value(DEFAULT_CONFIDENCE_PERCENT)
        self.detection_nms_slider.set_value(DEFAULT_DETECTION_NMS_PERCENT)
        self.association_slider.set_value(DEFAULT_ASSOCIATION_IOU_PERCENT)
        self.max_age_slider.set_value(DEFAULT_MAX_AGE)
        self.min_hits_slider.set_value(DEFAULT_MIN_HITS)
        self.trajectory_slider.set_value(DEFAULT_TRAJECTORY_LENGTH)
        self.ids_check.setChecked(DEFAULT_SHOW_IDS)
        self.trajectory_check.setChecked(DEFAULT_SHOW_TRAJECTORIES)
        self.class_list.blockSignals(True)
        for index in range(self.class_list.count()):
            self.class_list.item(index).setCheckState(Qt.CheckState.Checked)
        self.class_list.blockSignals(False)
        self._restoring = False
        if self.video_thread is not None and Path(self.model_path) != Path(MODEL_PATH):
            self.video_thread.set_model(MODEL_PATH)
        self._parameters_changed()
        self.status_label.setText("Parameters reset to defaults.")

    def _save_settings(self) -> None:
        if not hasattr(self, "trajectory_check"):
            return
        unchecked = [
            str(index)
            for index in range(self.class_list.count())
            if self.class_list.item(index).checkState() != Qt.CheckState.Checked
        ]
        self.settings.setValue("camera_index", self.camera_spin.value())
        self.settings.setValue("theme", self.theme)
        self.settings.setValue("model_path", self.model_path)
        self.settings.setValue("confidence_percent", self.confidence_slider.value())
        self.settings.setValue("detection_nms_percent", self.detection_nms_slider.value())
        self.settings.setValue("association_iou_percent", self.association_slider.value())
        self.settings.setValue("max_age", self.max_age_slider.value())
        self.settings.setValue("min_hits", self.min_hits_slider.value())
        self.settings.setValue("trajectory_length", self.trajectory_slider.value())
        self.settings.setValue("show_ids", self.ids_check.isChecked())
        self.settings.setValue("show_trajectories", self.trajectory_check.isChecked())
        self.settings.setValue("unchecked_classes", ",".join(unchecked))
        self.settings.sync()
        self.settings_label.setText("Settings: Saved")

    def _restore_settings(self) -> None:
        self._restoring = True
        s = self.settings
        self.camera_spin.blockSignals(True)
        self.camera_spin.setValue(s.value("camera_index", DEFAULT_CAMERA_INDEX, int))
        self.camera_spin.blockSignals(False)
        self.theme = str(s.value("theme", DEFAULT_THEME))
        saved_model = str(s.value("model_path", str(MODEL_PATH)))
        self.model_path = saved_model if Path(saved_model).is_file() else str(MODEL_PATH)
        self.model_label.setText(Path(self.model_path).name)
        self.model_label.setToolTip(self.model_path)
        self.confidence_slider.set_value(int(s.value("confidence_percent", DEFAULT_CONFIDENCE_PERCENT)))
        self.detection_nms_slider.set_value(int(s.value("detection_nms_percent", DEFAULT_DETECTION_NMS_PERCENT)))
        self.association_slider.set_value(int(s.value("association_iou_percent", DEFAULT_ASSOCIATION_IOU_PERCENT)))
        self.max_age_slider.set_value(int(s.value("max_age", DEFAULT_MAX_AGE)))
        self.min_hits_slider.set_value(int(s.value("min_hits", DEFAULT_MIN_HITS)))
        self.trajectory_slider.set_value(int(s.value("trajectory_length", DEFAULT_TRAJECTORY_LENGTH)))
        self.ids_check.setChecked(s.value("show_ids", DEFAULT_SHOW_IDS, bool))
        self.trajectory_check.setChecked(s.value("show_trajectories", DEFAULT_SHOW_TRAJECTORIES, bool))
        unchecked = str(s.value("unchecked_classes", "") or "")
        self.class_list.blockSignals(True)
        for token in unchecked.split(","):
            if token.strip().isdigit() and int(token) < self.class_list.count():
                self.class_list.item(int(token)).setCheckState(Qt.CheckState.Unchecked)
        self.class_list.blockSignals(False)
        self._restoring = False
        self.settings_label.setText("Settings: Restored")

    def closeEvent(self, event) -> None:
        if not self._closing:
            self._closing = True
            self._save_settings()
            self._stop_video_thread()
        event.accept()


def create_application() -> QApplication:
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    app.setOrganizationName(ORGANIZATION_NAME)
    app.setApplicationName(APP_NAME)
    return app
