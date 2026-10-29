# Lab09_MOT

Welcome to the ninth assignment of the Computer Vision and Machine Learning lab course!

This project provides a real-time PyQt6 application ("Multi-Object Tracking Playground") built around a pretrained YOLO detector. Detection is a black box: you do **not** train or modify it. The goal of this lab is to understand how detections of consecutive frames are linked into **tracks with persistent IDs**, using the simplest possible algorithm: an **IoU tracker**.

## 🎯 Assignment Objectives

In every frame the detector returns a list of boxes with no memory of the previous frame. Your tracker must decide which detection belongs to which known object, give new objects a new ID, and forget objects that disappeared. In this lab you will complete one method located in `mot.py`:

```
Tracker.update(detections)
```

Students should modify only `mot.py`. 

The expected processing pipeline is:

```
Camera Frame
     ↓
YOLO model + NMS (fixed, pretrained)
     ↓
Detections of this frame
     ↓
Tracker.update(detections)    ← your code
     ↓
IoU association → matched / missed / new tracks → delete old tracks
     ↓
Tracks with persistent IDs
```

## ✨ Features

- Real-time webcam (or video file) detection and tracking with PyQt6.
- Two synchronized views: **Detection View** (green detector boxes with YOLO confidence) and **Tracking View** (one color per track, track ID, and trajectory).
- Live tuning of the detector (confidence, NMS IoU) and of your tracker: association IoU threshold, maximum missed frames, minimum hits, trajectory length.
- Class filter (COCO by default), show/hide IDs, show/hide trajectories.
- **Choose your own model:** click the folder icon in the *Model* box to load any YOLOv5/YOLOv8-style `.onnx` detector from your computer (the default is `assets/yolov5s.onnx`). Class names are read from the model when available, the tracker restarts after a model change, and if a model cannot be loaded the previous one stays active.
- Lost tracks are drawn in gray at their last known position.
- Statistics panel: detections, active tracks, lost tracks, IDs created, FPS.
- Dark mode and light mode, full-screen mode, responsive scaling.
- Webcam and video-file input, camera-index selection, pause, restart, reset tracker, and a reset-to-default button.
- Settings are restored automatically between sessions.

## 🛠️ Setup & Installation

1. Clone the repository and navigate to the project directory.

2. Create a virtual environment (recommended):

```
python -m venv venv
```

Activate it on Linux/macOS:

```
source venv/bin/activate
```

On Windows PowerShell:

```
venv\Scripts\Activate.ps1
```

3. Install the required dependencies:

```
pip install -r requirements.txt
```

4. Make sure the model exists at `assets/yolov5s.onnx` (see `assets/README.md`).

5. Run the application:

```
python main.py
```

## 🎮 Using the Application

Until you finish `Tracker.update`, the **Detection View** works and the **Tracking View** shows no tracks (placeholder behavior). Move a person or object in front of the camera, or upload a video of people walking.

- **Association IoU:** minimum overlap between a track and a detection to be matched. Too high: fast objects get new IDs. Too low: different objects steal each other's IDs.
- **Max missed frames:** how long a track survives without a matching detection. Too small: identities break after short occlusions. Too large: ghost tracks stay.
- **Min hits:** how many matched frames a track needs before it is reported. It suppresses one-frame false detections.
- **IDs created:** if this number grows much faster than the number of real objects, your tracker is losing identities.

If your method raises an exception the application keeps running and shows the error in the status bar.

## 📂 Repository Structure

```
cvml-lab09-mot/
├── .gitignore
├── Readme.md
├── requirements.txt
├── main.py
├── gui.py
├── video_thread.py
├── detector.py
├── tracking_types.py
├── annotation.py
├── config.py
├── assets/
│   ├── README.md
│   └── yolov5s.onnx          # pretrained model (not part of the code you edit)
└── mot.py                    # The only file students should modify
```

### Module responsibilities

- `main.py` — application entry point only.
- `gui.py` — PyQt6 user interface, controls, themes, persistence, and rendering.
- `video_thread.py` — capture and real-time processing loop; calls the detector and your tracker.
- `detector.py` — ONNX model loading, pre-processing, decoding and detector NMS.
- `tracking_types.py` — `Detection`, `Track` and `compute_iou` used by your tracker.
- `annotation.py` — visualization of detections, track colors, IDs and trajectories.
- `config.py` — constants and shared parameter definitions.
- `mot.py` — `Tracker` class (`__init__` ready, `update` is your implementation).

## ⌨️ Keyboard Shortcuts

- `Space` — Pause / Resume
- `F11` — Full Screen / Windowed
- `R` — Reset Defaults
- `Q` — Quit
