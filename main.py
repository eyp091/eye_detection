import cv2
from logic.alert.alarm_system import AlertSystem
from logic.models.yolo_model import YoloModel
from logic.apps.start_web_app import startWebApp
import threading

cap = cv2.VideoCapture(0)

model_path = "assets/yolo_models/colab_yolov8_p3.pt"

model = YoloModel(model_path)

closed_eye_count = 0
alarm_triggered = False
tired_count = 0

while True:
    ret, frame = cap.read()

    if not ret:
        break

    results, annotated_frame = model.predict(frame)

    for result in results:
        for box in result.boxes:
            label = model.getLabel(box)

            if label == "opened eyes":
                closed_eye_count = 0
                alarm_triggered = False
            elif label == "closed eyes":
                closed_eye_count += 1

                if closed_eye_count >= 50 and not alarm_triggered:
                    threading.Thread(target=AlertSystem.playAlertSound).start()
                    alarm_triggered = True
                    tired_count += 1

                    if tired_count >= 1:
                        startWebApp()

    cv2.imshow("webcam", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()