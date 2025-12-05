def count_fingers(hand_landmarks):
    tips = [4, 8, 12, 16, 20]
    fingers = []

    # Thumb (x-axis logic)
    if hand_landmarks.landmark[tips[0]].x < hand_landmarks.landmark[tips[0] - 1].x:
        fingers.append(1)
    else:
        fingers.append(0)

    # Other fingers (y-axis logic)
    for tip in tips[1:]:
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y:
            fingers.append(1)
        else:
            fingers.append(0)

    return fingers.count(1)
