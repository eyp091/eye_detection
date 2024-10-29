import cv2
import threading
import torch
import itertools

from logic.alert.alarm_system import AlertSystem
from logic.models.yolo_model import YoloModel
from logic.apps.start_web_app import startWebApp
from logic.model_logic.check_model_status import checkEyeStatus, checkYawnStatus
from logic.models.load_yolo_models import loadModels

def processVideoStream(eye_model, yawn_model):
    cap = cv2.VideoCapture(0)
    counts = {'closed_eye_count': 0, 'tired_count': 0, 'alarm_triggered': False}
    counts_yawn = {'yawn_count': 0}
    while True:
        ret, frame = cap.read()

        if not ret: break

        eye_results, _ = eye_model.predict(frame)
        yawn_results, _ = yawn_model.predict(frame)

        # göz durumunu kontrol et
        checkEyeStatus(eye_results, eye_model, counts, frame)

        #esneme durumunu kontrol et
        checkYawnStatus(yawn_results, yawn_model, counts_yawn, frame)
        cv2.imshow("webcam", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

def main():
    eye_model, yawn_model = loadModels()
    processVideoStream(eye_model, yawn_model)

if __name__ == "__main__":
    main()