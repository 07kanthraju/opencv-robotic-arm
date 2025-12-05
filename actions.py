import time
import threading

motion_lock = threading.Lock()

# --- Servo and Motion Parameters ---
neutral_angle = 90
hold_time_14 = 1.0

base_channel = 15
base_angle = 90    # starting position
base_step = 45     # degrees per cycle
base_min = 90
base_max = 180


# --- Helper: Base Rotation ---
def rotate_base(servo):
    """Rotate the base servo by +45° each cycle and reset after 180°."""
    global base_angle

    # Increment base rotation
    base_angle += base_step
    if base_angle > base_max:
        base_angle = base_min  # reset after full sweep

    servo.send_command(base_channel, base_angle)
    print(f"🔄 Base rotated to {base_angle}°")


# --- Reset all servos ---
def reset_all_servos(servo):
    with motion_lock:
        for ch in [0, 2, 6, 9, 14, base_channel]:
            servo.send_command(ch, neutral_angle)
        print("🤚 All servos reset to neutral.")


# --- Gesture-based actions ---
def action_one_finger(servo):
    with motion_lock:
        servo.send_command(0, 45)
        print("👉 1 finger → Servo 0 → 45°")


def action_two_fingers(servo):
    with motion_lock:
        servo.send_command(2, 180)
        print("✌️ 2 fingers → Servo 2 → 180°")


def action_three_fingers(servo):
    with motion_lock:
        servo.send_command(6, 40)
        print("🤟 3 fingers → Servo 6 → 40°")


def action_four_fingers(servo):
    with motion_lock:
        servo.send_command(9, 45)
        print("🖖 4 fingers → Servo 9 → 45°")


def action_five_fingers(servo):
    with motion_lock:
        print("⭐ 5 fingers → Pick-up + Base rotation")

        # Step 1: Pick-up motion (servo 14)
        servo.send_command(14, 150)
        time.sleep(hold_time_14)
        servo.send_command(14, 65)
        time.sleep(10)
        # servo.send_command(14, neutral_angle)
        time.sleep(0.5)

        # Step 2: Rotate base after pick-up
        rotate_base(servo)


# --- Gesture → Action mapping ---
gesture_actions = {
    0: reset_all_servos,
    1: action_one_finger,
    2: action_two_fingers,
    3: action_three_fingers,
    4: action_four_fingers,
    5: action_five_fingers
}
