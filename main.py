import cv2
import mediapipe as mp
import serial
import math
from mercurial.wireprotoframing import frame

# webcam setup
webcam = cv2.VideoCapture(0)
webcam.set(3, 1280)
webcam.set(4, 720)

mp_pose = mp.solutions.pose
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Uncomment and set your correct COM port
# my_arduino = serial.Serial("COM3", 9600)

def send_signal_to_arduino(distance):  # Arm movement control
    if 0 < distance < 250:
        # my_arduino.write(b'A')
        print("Signal: A (Close)")
    elif 250 < distance < 450:
        # my_arduino.write(b'B')
        print("Signal: B (Mid)")
    elif distance > 450:
        # my_arduino.write(b'C')
        print("Signal: C (Far)")

def send_palm_signal(gesture):  # Palm open/close signal
    if gesture == "Open":
        # my_arduino.write(b'O')
        print("Palm Open - Signal: O")
    elif gesture == "Closed":
        # my_arduino.write(b'F')
        print("Palm Closed - Signal: F")

def detect_palm_state(hand_landmarks, height):
    """
    Simple palm gesture detection: open hand vs closed fist.
    Uses vertical positions of finger tips and PIP joints.
    """
    tip_ids = [4, 8, 12, 16, 20]  # Thumb, Index, Middle, Ring, Pinky tips
    fingers_up = 0

    for tip_id in tip_ids[1:]:  # Skip thumb for simplicity
        tip_y = hand_landmarks.landmark[tip_id].y * height
        pip_y = hand_landmarks.landmark[tip_id - 2].y * height
        if tip_y < pip_y:
            fingers_up += 1

    if fingers_up >= 4:
        return "Open"
    elif fingers_up == 0:
        return "Closed"
    else:
        return "Partial"

# Pose and Hand tracking setup
with mp_pose.Pose(static_image_mode=True, 
                  min_detection_confidence=0.5, 
                  min_tracking_confidence=0.5) as pose, \
     mp_hands.Hands(max_num_hands=1, 
                    min_detection_confidence=0.5, 
                    min_tracking_confidence=0.5) as hands:

    while True:
        control, frame = webcam.read()
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        height, width, _ = frame.shape

        result = pose.process(rgb)
        hand_result = hands.process(rgb)

        # ARM DETECTION (unchanged from your code)
        if result.pose_landmarks:
            wrist = result.pose_landmarks.landmark[16]
            x1 = int(wrist.x * width)
            y1 = int(wrist.y * height)
            cv2.circle(frame, (x1, y1), 20, (0, 0, 225), -1)

            elbow = result.pose_landmarks.landmark[14]
            x2 = int(elbow.x * width)
            y2 = int(elbow.y * height)
            cv2.circle(frame, (x2, y2), 20, (0, 0, 225), -1)

            shoulder = result.pose_landmarks.landmark[12]
            x3 = int(shoulder.x * width)
            y3 = int(shoulder.y * height)
            cv2.circle(frame, (x3, y3), 20, (0, 0, 225), -1)

            cv2.line(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
            cv2.line(frame, (x2, y2), (x3, y3), (255, 0, 0), 2)

            distance = math.sqrt(math.pow(x3 - x1, 2) + math.pow(y3 - y1, 2))
            print("Arm Distance:", distance)
            send_signal_to_arduino(distance)

        # PALM DETECTION (new feature)
        if hand_result.multi_hand_landmarks:
            for hand_landmarks in hand_result.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                gesture = detect_palm_state(hand_landmarks, height)
                send_palm_signal(gesture)
                cv2.putText(frame, f"Palm: {gesture}", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 
                            1, (0, 255, 0), 2)

        cv2.imshow("Arm + Palm Detector", frame)
        if cv2.waitKey(10) == 27:
            break

webcam.release()
cv2.destroyAllWindows()
