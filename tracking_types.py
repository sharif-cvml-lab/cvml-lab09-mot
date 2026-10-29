"""Fixed infrastructure: data structures shared by the tracker and the GUI.

Students do not modify this file.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

MAX_TRAJECTORY_POINTS = 300


@dataclass(frozen=True)
class Detection:
    """One detector output for the current frame."""

    box: np.ndarray  # shape (4,), pixel coordinates (x1, y1, x2, y2)
    score: float     # detector confidence
    class_id: int    # COCO class index


class Track:
    """One tracked object. The tracker keeps one Track per identity."""

    def __init__(self, track_id: int, detection: Detection):
        self.id = track_id
        self.box = np.asarray(detection.box, dtype=np.float32).copy()
        self.score = float(detection.score)
        self.class_id = int(detection.class_id)
        self.hits = 1     # number of frames in which the track was matched (including birth)
        self.age = 1      # number of frames since birth
        self.missed = 0   # consecutive frames without a matched detection
        self.trajectory: list[tuple[float, float]] = [self.center]

    @property
    def center(self) -> tuple[float, float]:
        return float((self.box[0] + self.box[2]) / 2), float((self.box[1] + self.box[3]) / 2)

    def update(self, detection: Detection) -> None:
        """Call when a detection was matched to this track in the current frame."""
        self.box = np.asarray(detection.box, dtype=np.float32).copy()
        self.score = float(detection.score)
        self.hits += 1
        self.age += 1
        self.missed = 0
        self.trajectory.append(self.center)
        if len(self.trajectory) > MAX_TRAJECTORY_POINTS:
            self.trajectory.pop(0)

    def mark_missed(self) -> None:
        """Call when no detection was matched to this track in the current frame."""
        self.age += 1
        self.missed += 1


def compute_iou(box_a: np.ndarray, box_b: np.ndarray) -> float:
    """IoU of two (x1, y1, x2, y2) boxes."""
    x1 = max(box_a[0], box_b[0])
    y1 = max(box_a[1], box_b[1])
    x2 = min(box_a[2], box_b[2])
    y2 = min(box_a[3], box_b[3])
    intersection = max(0.0, x2 - x1) * max(0.0, y2 - y1)
    area_a = (box_a[2] - box_a[0]) * (box_a[3] - box_a[1])
    area_b = (box_b[2] - box_b[0]) * (box_b[3] - box_b[1])
    union = area_a + area_b - intersection
    return float(intersection / union) if union > 0 else 0.0
