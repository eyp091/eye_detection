import cv2
import itertools
import threading
from logic.alert.alarm_system import AlertSystem
import numpy as np

def draw_fancy_box(frame, x1, y1, x2, y2, color, label, thickness=2):
    # Kutu köşeleri için boyut
    corner_length = 20
    
    # Yarı saydam overlay için kutu çizimi
    overlay = frame.copy()
    cv2.rectangle(overlay, (x1, y1), (x2, y2), color, -1)
    cv2.addWeighted(overlay, 0.15, frame, 0.85, 0, frame)  # Saydamlık arttırıldı

    # Köşe çizgileri
    # Sol üst köşe
    cv2.line(frame, (x1, y1), (x1 + corner_length, y1), color, 1)  # İnce çizgi
    cv2.line(frame, (x1, y1), (x1, y1 + corner_length), color, 1)
    
    # Sağ üst köşe
    cv2.line(frame, (x2, y1), (x2 - corner_length, y1), color, 1)
    cv2.line(frame, (x2, y1), (x2, y1 + corner_length), color, 1)
    
    # Sol alt köşe
    cv2.line(frame, (x1, y2), (x1 + corner_length, y2), color, 1)
    cv2.line(frame, (x1, y2), (x1, y2 - corner_length), color, 1)
    
    # Sağ alt köşe
    cv2.line(frame, (x2, y2), (x2 - corner_length, y2), color, 1)
    cv2.line(frame, (x2, y2), (x2, y2 - corner_length), color, 1)

    # Etiket için arka plan
    (label_width, label_height), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)  # Font boyutu küçültüldü
    cv2.rectangle(frame, (x1, y1 - 25), (x1 + label_width + 10, y1), color, -1)
    
    # Etiket metni
    cv2.putText(frame, label, (x1 + 5, y1 - 8), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)  # İnce yazı

def checkStatus(results, model, counts, frame):
    # Soft renk paleti (BGR formatında)
    COLORS = {
        'open_eye': (176, 224, 170),     # Soft yeşil
        'closed_eye': (147, 147, 255),   # Soft kırmızı
        'open_mouth': (200, 174, 161),   # Soft turuncu
        'closed_mouth': (216, 181, 224)  # Soft mor
    }
    
    LABELS = {
        'open_eye': 'Eyes Open',
        'closed_eye': 'Eyes Closed',
        'open_mouth': 'Yawning',
        'closed_mouth': 'Mouth Closed'
    }

    all_boxes = itertools.chain.from_iterable(result.boxes for result in results)

    for box in all_boxes:
        label = model.getLabel(box)
        x1, y1, x2, y2 = map(int, box.xyxy[0])

        if label == "open_eye":
            counts['closed_eye_count'] = 0
            counts['alarm_triggered'] = False
            draw_fancy_box(frame, x1, y1, x2, y2, COLORS[label], LABELS[label])

        elif label == "closed_eye":
            counts['closed_eye_count'] += 1
            draw_fancy_box(frame, x1, y1, x2, y2, COLORS[label], LABELS[label])

        elif label == "open_mouth":
            counts['yawn_count'] += 1
            draw_fancy_box(frame, x1, y1, x2, y2, COLORS[label], LABELS[label])

        elif label == "closed_mouth":
            draw_fancy_box(frame, x1, y1, x2, y2, COLORS[label], LABELS[label])

        # Yorgunluk durumu kontrolü
        if counts['closed_eye_count'] >= 50 and not counts['alarm_triggered']:
            threading.Thread(target=AlertSystem.playAlertSound).start()
            counts['alarm_triggered'] = True
            counts['tired_count'] += 1
<<<<<<< HEAD

            if counts['tired_count'] >= 1:
                startWebApp()
=======
>>>>>>> 4be4a4ed0f96bb019eb8e5e468834e38762aad3d
