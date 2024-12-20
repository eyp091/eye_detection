import cv2
import itertools
import threading
from logic.alert.alarm_system import AlertSystem

def checkStatus(results, model, counts, frame):
    all_boxes = itertools.chain.from_iterable(result.boxes for result in results)

    for box in all_boxes:
        label = model.getLabel(box)

        if label == "open_eye":
            counts['closed_eye_count'] = 0
            counts['alarm_triggered'] = False

            x1, y1, x2, y2 = map(int, box.xyxy[0])
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, "Opened Eyes", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        elif label == "closed_eye":
            counts['closed_eye_count'] += 1

            x1, y1, x2, y2 = map(int, box.xyxy[0])
            cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
            cv2.putText(frame, "Closed Eyes", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

        elif label == "open_mouth":
            counts['yawn_count'] += 1

            x1, y1, x2, y2 = map(int, box.xyxy[0])
            cv2.rectangle(frame, (x1, y1), (x2, y2), (49, 62, 246), 2)
            cv2.putText(frame, "Open Mouth", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (49, 62, 246), 2)

        elif label == "closed_mouth":
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 255), 2)  # Mor renk (255, 0, 255)
            cv2.putText(frame, "Closed Mouth", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 2)  # Mor renk (255, 0, 255)


        #check the fatigue status
        if counts['closed_eye_count'] >= 50  and not counts['alarm_triggered']:
            threading.Thread(target=AlertSystem.playAlertSound).start()
            counts['alarm_triggered'] = True
            counts['tired_count'] += 1
