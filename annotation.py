from __future__ import annotations

import colorsys

import cv2
import numpy as np

from config import COCO_CLASSES, LOST_COLOR


def _class_name(class_id: int, class_names) -> str:
    names = class_names if class_names is not None else COCO_CLASSES
    return names[class_id] if 0 <= class_id < len(names) else f"class {class_id}"
from tracking_types import Track


def track_color(track_id: int) -> tuple[int, int, int]:
    """Deterministic, well-separated BGR color for each track ID."""
    hue = (track_id * 0.618033988749895) % 1.0
    r, g, b = colorsys.hsv_to_rgb(hue, 0.85, 1.0)
    return int(b * 255), int(g * 255), int(r * 255)


def annotate_detections(
    frame: np.ndarray,
    boxes: np.ndarray,
    scores: np.ndarray,
    class_ids: np.ndarray,
    color: tuple[int, int, int],
    thickness: int = 2,
    class_names=None,
) -> np.ndarray:
    """Draw detector boxes with 'class confidence' labels on a copy of the frame."""
    output = frame.copy()
    for box, score, class_id in zip(boxes, scores, class_ids):
        x1, y1, x2, y2 = (int(round(v)) for v in box)
        cv2.rectangle(output, (x1, y1), (x2, y2), color, thickness)
        label = f"{_class_name(int(class_id), class_names)} {float(score):.2f}"
        cv2.putText(output, label, (x1, max(20, y1 - 8)), cv2.FONT_HERSHEY_SIMPLEX,
                    0.55, color, 2, cv2.LINE_AA)
    return output


def annotate_tracks(
    frame: np.ndarray,
    tracks: list[Track],
    show_ids: bool,
    show_trajectories: bool,
    trajectory_length: int,
) -> np.ndarray:
    """Draw tracks: one color per ID, ID labels and recent trajectories.

    Tracks that are currently lost (missed > 0) are drawn in gray at their last known position.
    """
    output = frame.copy()
    for track in tracks:
        lost = track.missed > 0
        color = LOST_COLOR if lost else track_color(track.id)

        if show_trajectories and len(track.trajectory) > 1:
            points = np.asarray(track.trajectory[-trajectory_length:], dtype=np.int32).reshape(-1, 1, 2)
            cv2.polylines(output, [points], False, color, 2, cv2.LINE_AA)

        x1, y1, x2, y2 = (int(round(v)) for v in track.box)
        cv2.rectangle(output, (x1, y1), (x2, y2), color, 1 if lost else 2)
        if show_ids:
            label = f"ID {track.id}" + (" lost" if lost else "")
            cv2.putText(output, label, (x1, max(20, y1 - 8)), cv2.FONT_HERSHEY_SIMPLEX,
                        0.6, color, 2, cv2.LINE_AA)
    return output
