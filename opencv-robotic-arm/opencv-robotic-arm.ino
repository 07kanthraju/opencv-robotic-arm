#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();

#define SERVOMIN 150
#define SERVOMAX 600
#define SERVO_FREQ 60

int currentAngle[16];

// Convert an angle (0–180°) to PCA9685 pulse value
int angleToPulse(int angle) {
  return map(angle, 0, 180, SERVOMIN, SERVOMAX);
}

// Smoothly move servo from current position to target
void smoothMove(int ch, int target) {
  int start = currentAngle[ch];
  target = constrain(target, 0, 180);
  int step = (target > start) ? 1 : -1;

  for (int pos = start; pos != target; pos += step) {
    pwm.setPWM(ch, 0, angleToPulse(pos));
    delay(10);
  }

  pwm.setPWM(ch, 0, angleToPulse(target));
  currentAngle[ch] = target;
  delay(200);
}

void setup() {
  Serial.begin(9600);
  pwm.begin();
  pwm.setPWMFreq(SERVO_FREQ);
  delay(500);

  // Initialize servos (channels 0,2,6,9,14,15)
  int channels[] = {0, 2, 6, 9, 14, 15};
  for (int i = 0; i < 6; i++) {
    int ch = channels[i];
    currentAngle[ch] = 90;
    pwm.setPWM(ch, 0, angleToPulse(90));
    delay(200);
  }

  Serial.println("✅ 6-Servo Smooth Controller Ready (Base included)");
  Serial.println("Use: S,<channel>,<angle> or S,ALL,<angle>");
}

void loop() {
  if (Serial.available()) {
    String line = Serial.readStringUntil('\n');
    line.trim();

    if (line.startsWith("S,")) {
      // Handle "S,ALL,<angle>"
      if (line.startsWith("S,ALL,")) {
        int target = line.substring(6).toInt();
        int channels[] = {0, 2, 6, 9, 14, 15};
        for (int i = 0; i < 6; i++) {
          smoothMove(channels[i], target);
        }
        Serial.print("➡ ALL moved to ");
        Serial.println(target);
        return;
      }

      // Handle "S,<channel>,<angle>"
      int comma = line.indexOf(',', 2);
      if (comma == -1) return;

      int ch = line.substring(2, comma).toInt();
      int angle = line.substring(comma + 1).toInt();
      angle = constrain(angle, 0, 180);

      smoothMove(ch, angle);
      Serial.print("Servo ");
      Serial.print(ch);
      Serial.print(" → ");
      Serial.println(angle);
    }
  }
}
