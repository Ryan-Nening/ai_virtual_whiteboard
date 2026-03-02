import cv2
from ursina import Ursina, Button, scene, color, destroy, mouse
from ursina.prefabs.first_person_controller import FirstPersonController
import mediapipe
import math

application_engine = Ursina()

video_capture = cv2.VideoCapture(0)
mediapipe_hands = mediapipe.solutions.hands
hand_tracker = mediapipe_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
previous_pinch_state = False

application_engine.run()
