import cv2
import threading
import torch
import asyncio
import websockets
import json

from logic.model_logic.check_model_status import checkStatus
from logic.models.load_yolo_models import loadModels

def processVideoStream(eye_model):
    cap = cv2.VideoCapture(0)
    counts = {'closed_eye_count': 0, 'tired_count': 0, 'yawn_count': 0, 'alarm_triggered': False}
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        eye_results, _ = eye_model.predict(frame)
        checkStatus(eye_results, eye_model, counts, frame)
        
        shared_status["status"] = counts
        print("closed eye: ", counts["closed_eye_count"])
        
        cv2.imshow("webcam", frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()


def main():
    eye_model = loadModels()
    processVideoStream(eye_model)


if __name__ == "__main__":
    main()
