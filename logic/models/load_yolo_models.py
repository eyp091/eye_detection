from logic.utils.config import eye_model_path
from models.yolo_model import YoloModel

def loadModels():
    eye_model = YoloModel(eye_model_path)

    return eye_model