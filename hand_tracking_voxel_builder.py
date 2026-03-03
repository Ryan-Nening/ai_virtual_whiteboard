import cv2
from ursina import Ursina, Button, scene, color, destroy, mouse
from ursina.prefabs.first_person_controller import FirstPersonController
import mediapipe as mp
import math

application_engine = Ursina()
video_capture = cv2.VideoCapture(0)

mp_hands = mp.solutions.hands
hand_tracker = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
previous_pinch_state = False

class VoxelBlock(Button):
    def __init__(self, position=(0, 0, 0)):
        super().__init__(parent=scene, position=position, model='cube', origin_y=0.5, texture='white_cube')

    def input(self, key_press):
        if self.hovered:
            if key_press == 'left mouse down':
                new_voxel_position = self.position + mouse.normal
                voxel_block = VoxelBlock(position=new_voxel_position)
            if key_press == 'right mouse down':
                destroy(self)

def update():
    global previous_pinch_state
    
    success, image = video_capture.read()
    if not success: return

    image = cv2.flip(image, 1)
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hand_tracker.process(rgb_image)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            itip = hand_landmarks.landmark[8]
            ttip = hand_landmarks.landmark[4]

            # Calculate the distance between thumb and index finger
            dist = math.sqrt((itip.x - ttip.x)**2 + (itip.y - ttip.y)**2)
            is_pinching = dist < 0.05

            if is_pinching and not previous_pinch_state:
                # Move the virtual mouse to your finger tip
                mouse.position = (itip.x - 0.5, (1 - itip.y) - 0.5)
                if mouse.hovered_entity:
                    VoxelBlock(position=mouse.hovered_entity.position + mouse.normal)

            previous_pinch_state = is_pinching

    cv2.imshow("Hand Cam", image)

for z in range(20):
    for x in range(20):
        voxel = VoxelBlock(position=(x, 0, z))

player = FirstPersonController()
application_engine.run()