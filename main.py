import threading
import cv2
import time
from camera_module import HandTracker
from gesture_module import count_fingers
from servo_controller import ServoController
from actions import gesture_actions, motion_lock
from language_module import interpret_command

def execute_openai_actions(servo, actions):
    """Execute servo actions returned by OpenAI."""
    with motion_lock:
        for act in actions:
            servo.send_command(act["servo"], act["angle"])
            time.sleep(0.3)

def main():
    servo = ServoController("/dev/ttyUSB0", 9600)
    tracker = HandTracker()
    last_finger_count = -1

    print("✅ VLA System Started — type a command at any time.")
    print("💬 Example: 'pick up the object', 'rotate base', 'reset all'")

    while True:
        frame, result = tracker.get_frame()
        if frame is None:
            continue

        finger_count = 0
        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                tracker.draw_landmarks(frame, hand_landmarks)
                finger_count = count_fingers(hand_landmarks)

        cv2.putText(frame, f"Fingers: {finger_count}", (30, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3)
        tracker.show(frame)

        # Gesture handling (existing)
        if finger_count != last_finger_count and not motion_lock.locked():
            print(f"🖐 Gesture detected: {finger_count} fingers")
            threading.Thread(target=gesture_actions[finger_count], args=(servo,)).start()
            last_finger_count = finger_count

        # --- Language Input ---
        if cv2.waitKey(1) & 0xFF == ord('c'):  # press 'c' to enter a command
            user_input = input("\n💬 Enter command: ")
            context = f"{finger_count} fingers shown"
            actions = interpret_command(user_input, context)
            if actions:
                print(f"🧠 OpenAI decided actions: {actions}")
                threading.Thread(target=execute_openai_actions, args=(servo, actions)).start()

        if cv2.waitKey(1) & 0xFF == 27:  # ESC to exit
            print("🛑 Exiting...")
            break

    tracker.release()
    servo.close()

if __name__ == "__main__":
    main()
