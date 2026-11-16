# assets/

Put pretrained detector here as `yolov5s.onnx`:
How to produce it :

```
git clone https://github.com/ultralytics/yolov5
cd yolov5
pip install -r requirements.txt
python export.py --weights yolov5s.pt --include onnx --imgsz 640 --opset 12
```