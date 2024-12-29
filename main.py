import cv2
<<<<<<< HEAD
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
=======
import socketio
import time
from logic.model_logic.check_model_status import checkStatus
from logic.models.load_yolo_models import loadModels

sio = socketio.Client()

client_message = ""

@sio.event
def connect():
    print("Sunucuya bağlanıldı!")

@sio.event
def status(data):
    global client_message
    client_message = data.get("message", "mesaj alındı")

    if client_message == "closed":
        print("Client kapalı durumu alındı, işlem sonlandırılıyor.")
        sio.disconnect() 
        exit() 

@sio.event
def disconnect():
    print("Bağlantı kesildi!")

def processVideoStreamAndSendMessages(eye_model):
    cap = cv2.VideoCapture(0)  
    counts = {'closed_eye_count': 0, 'tired_count': 0, 'yawn_count': 0, 'alarm_triggered': False}
    global client_message, message_flag
    try:
        while True:
            if client_message == "closed":
                print("Client kapalı durumu alındı, işlem sonlandırılıyor.")
                break

            ret, frame = cap.read()
            if not ret:
                print("Kamera akışı sonlandırıldı.")
                break

            eye_results, _ = eye_model.predict(frame)
            checkStatus(eye_results, eye_model, counts, frame)

            print(f"mesaj: {client_message}")

            if counts['tired_count'] > 0:
                sio.emit('status', {"message": "yorgun"})
            else:
                sio.emit('status', {"message": "normal"})

            cv2.imshow("webcam", frame)  
            if cv2.waitKey(1) & 0xFF == ord('q'): 
                print("Kamera akışı durduruldu.")
                break
            
    finally:
        cap.release()
        cv2.destroyAllWindows()
>>>>>>> 4be4a4ed0f96bb019eb8e5e468834e38762aad3d


def main():
<<<<<<< HEAD
    eye_model = loadModels()
    processVideoStream(eye_model)
=======
    eye_model = loadModels() 
>>>>>>> 4be4a4ed0f96bb019eb8e5e468834e38762aad3d

    sio.connect('http://localhost:3000')

    processVideoStreamAndSendMessages(eye_model)

    sio.disconnect()

if __name__ == "__main__":
    main()
