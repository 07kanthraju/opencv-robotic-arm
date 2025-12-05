import cv2
import mediapipe as mp
import os

# Environment fixes
os.environ["QT_QPA_PLATFORM"] = "xcb"
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
os.environ["TF_FORCE_GPU_ALLOW_GROWTH"] = "false"

class HandTracker:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            raise RuntimeError("Camera not found!")
        self.mp_hands = mp.solutions.hands
        self.mp_draw = mp.solutions.drawing_utils
        self.hands = self.mp_hands.Hands(
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.6
        )
        cv2.namedWindow("Gesture Control", cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty("Gesture Control", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    def get_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return None, None
        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = self.hands.process(rgb)
        return frame, result

    def draw_landmarks(self, frame, hand_landmarks):
        self.mp_draw.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)

    def show(self, frame):
        cv2.imshow("Gesture Control", frame)

    def release(self):
        self.cap.release()
        cv2.destroyAllWindows()
