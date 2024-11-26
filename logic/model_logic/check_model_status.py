import cv2
import itertools
import threading
from logic.alert.alarm_system import AlertSystem
from logic.apps.start_web_app import startWebApp

def checkStatus(results, model, counts, frame, check_type="eye"):
    all_boxes = itertools.chain.from_iterable(result.boxes for result in results)

    for box in all_boxes:
        label = model.getLabel(box)

        #check eye status
        if check_type == "eye":
            if label == "opened eyes":
                counts['closed_eye_count'] = 0
                counts['alarm_triggered'] = False

                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, "Opened Eyes", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            elif label == "closed eyes":
                counts['closed_eye_count'] += 1

                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
                cv2.putText(frame, "Closed Eyes", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

        #check yawn status
        elif check_type == "yawn":
            if label == "yawn":
                counts['yawn_count'] += 1

                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cv2.rectangle(frame, (x1, y1), (x2, y2), (49, 62, 246), 2)
                cv2.putText(frame, "Yawn", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (49, 62, 246), 2)

        #check the fatigue status
        if counts['closed_eye_count'] >= 50 and counts['yawn_count'] >= 50 and not counts['alarm_triggered']:
            threading.Thread(target=AlertSystem.playAlertSound).start()
            counts['alarm_triggered'] = True
            counts['tired_count'] += 1

            if counts['tired_count'] >= 2:
                startWebApp()
