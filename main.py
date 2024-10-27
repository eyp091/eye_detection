import cv2
from logic.alert.alarm_system import AlertSystem
from logic.models.yolo_model import YoloModel
from logic.apps.start_web_app import startWebApp
from logic.utils.config import eye_model_path, yawn_model_path
import threading
import torch
import itertools


def loadModel(): 
    eye_model = YoloModel(eye_model_path)
    yawn_model = YoloModel(yawn_model_path)
    return eye_model, yawn_model

def checkEyeStatus(eye_results, eye_model, counts):

    all_boxes = itertools.chain.from_iterable(result.boxes for result in eye_results)

    for box in all_boxes:
        label = eye_model.getLabel(box)

        if label == "opened eyes":
            counts['closed_eye_count'] = 0
            counts['alarm_triggered'] = False
        elif label == "closed eyes":
            counts['closed_eye_count'] += 1

            if counts['closed_eye_count'] >=50 and not counts['alarm_triggered']:
                threading.Thread(target=AlertSystem.playAlertSound).start()
                counts['alarm_triggered'] = True
                counts['tired_count'] += 1

                if counts['tired_count'] >= 1:
                    startWebApp()

def checkYawnStatus(yawn_results, yawn_model, counts):

    all_boxes = itertools.chain.from_iterable(result.boxes for result in yawn_results)

    for box in all_boxes:
        label = yawn_model.getLabel(box)

        if label == "yawn":
            counts['yawn_count'] += 1
            print("yawn: ", counts['yawn_count']) 

def processVideoStream(eye_model, yawn_model):
    cap = cv2.VideoCapture(0)
    counts = {'closed_eye_count': 0, 'tired_count': 0, 'alarm_triggered': False}
    counts_yawn = {'yawn_count': 0}
    while True:
        ret, frame = cap.read()

        if not ret: break

        eye_results, eye_frame = eye_model.predict(frame)
        yawn_results, _ = yawn_model.predict(frame)

        # göz durumunu kontrol et
        checkEyeStatus(eye_results, eye_model, counts)

        #esneme durumunu kontrol et
        checkYawnStatus(yawn_results, yawn_model, counts_yawn)
        cv2.imshow("webcam", eye_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

def main():
    eye_model, yawn_model = loadModel()
    processVideoStream(eye_model, yawn_model)

if __name__ == "__main__":
    main()