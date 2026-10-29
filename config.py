from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

APP_NAME = "CVML Lab 09 - Multi-Object Tracking"
ORGANIZATION_NAME = "Sharif CVML Lab"

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "assets" / "yolov5s.onnx"
INPUT_SIZE = 640

CAPTURE_WIDTH = 640
CAPTURE_HEIGHT = 480
TARGET_FPS = 30

DEFAULT_CAMERA_INDEX = 0
DEFAULT_THEME = "dark"

DEFAULT_CONFIDENCE_PERCENT = 40
DEFAULT_DETECTION_NMS_PERCENT = 45
DEFAULT_ASSOCIATION_IOU_PERCENT = 30
DEFAULT_MAX_AGE = 15          # maximum consecutive missed frames
DEFAULT_MIN_HITS = 3          # matched frames before a track is reported
DEFAULT_TRAJECTORY_LENGTH = 40
DEFAULT_SHOW_IDS = True
DEFAULT_SHOW_TRAJECTORIES = True

DEFAULT_SETTINGS_MESSAGE = "Settings: Ready"

DETECTION_COLOR = (60, 220, 140)   # BGR, green
LOST_COLOR = (150, 150, 150)       # BGR, gray

IMAGE_EXTENSIONS = (".png", ".jpg", ".jpeg", ".bmp", ".webp", ".tif", ".tiff")
VIDEO_EXTENSIONS = (".mp4", ".avi", ".mov", ".mkv", ".webm", ".m4v")

FILE_FILTER = (
    "Media Files (*.png *.jpg *.jpeg *.bmp *.webp *.tif *.tiff "
    "*.mp4 *.avi *.mov *.mkv *.webm *.m4v);;"
    "Images (*.png *.jpg *.jpeg *.bmp *.webp *.tif *.tiff);;"
    "Videos (*.mp4 *.avi *.mov *.mkv *.webm *.m4v);;"
    "All Files (*)"
)

COCO_CLASSES = [
    "person", "bicycle", "car", "motorcycle", "airplane", "bus", "train", "truck", "boat",
    "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat",
    "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack",
    "umbrella", "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball",
    "kite", "baseball bat", "baseball glove", "skateboard", "surfboard", "tennis racket",
    "bottle", "wine glass", "cup", "fork", "knife", "spoon", "bowl", "banana", "apple",
    "sandwich", "orange", "broccoli", "carrot", "hot dog", "pizza", "donut", "cake", "chair",
    "couch", "potted plant", "bed", "dining table", "toilet", "tv", "laptop", "mouse",
    "remote", "keyboard", "cell phone", "microwave", "oven", "toaster", "sink",
    "refrigerator", "book", "clock", "vase", "scissors", "teddy bear", "hair drier",
    "toothbrush",
]


@dataclass(frozen=True)
class TrackingParameters:
    confidence_threshold: float
    detection_nms_threshold: float
    iou_threshold: float
    max_age: int
    min_hits: int
    trajectory_length: int
    class_filter: tuple[int, ...] | None  # None = all classes
    show_ids: bool
    show_trajectories: bool
