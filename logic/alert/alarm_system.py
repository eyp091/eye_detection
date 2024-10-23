import pygame

alert_sound = './assets/sounds/uyari_sesi.mp3'

class AlertSystem:
    def playAlertSound():
        pygame.mixer.init()
        pygame.mixer.music.load(alert_sound)
        pygame.mixer.music.play()