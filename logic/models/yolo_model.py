import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from ultralytics import YOLO

class YoloModel:
    def __init__(self, model_path):
        self.model = YOLO(model_path, verbose=False)

    def predict(self, frame):
        results = self.model(frame, verbose=False)
        annotated_frame = results[0].plot()
        return results, annotated_frame

    def getLabel(self, box):
        cls = box.cls
        return self.model.names[int(cls)]