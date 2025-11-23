#include <Wire.h>
#include <Servo.h>
#include <Adafruit_PWMServoDriver.h>

Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();
char incomingData;

Servo servo1; // Base rotation
Servo servo2; // Shoulder
Servo servo3; // Elbow
Servo servo4; // Wrist
Servo servo5; // Gripper
Servo servo6; // Optional (extra motor)

void setup() {
  Serial.begin(9600); // Serial communication with Python
  pwm.begin();
  pwm.setPWMFreq(60); // Typical servo frequency

  // Attach servos to pins (you can change as needed)
  servo1.attach(3);
  servo2.attach(5);
  servo3.attach(6);
  servo4.attach(9);
  servo5.attach(10);
  servo6.attach(11);

  // Initial neutral positions
  servo1.write(90);
  servo2.write(90);
  servo3.write(90);
  servo4.write(90);
  servo5.write(90);
  servo6.write(90);
}

void loop() {
  if (Serial.available()) {
    incomingData = Serial.read();

    // --- Arm Movement Commands ---
    if (incomingData == 'A') {
      servo1.write(45);   // Base rotate close
      servo2.write(60);   // Shoulder close
      servo3.write(70);   // Elbow close
      Serial.println("Arm Close");
    }
    else if (incomingData == 'B') {
      servo1.write(90);   // Mid position
      servo2.write(90);
      servo3.write(90);
      Serial.println("Arm Mid");
    }
    else if (incomingData == 'C') {
      servo1.write(135);  // Arm extended
      servo2.write(120);
      servo3.write(110);
      Serial.println("Arm Far");
    }

    // --- Palm Gesture Commands ---
    if (incomingData == 'O') {
      servo5.write(0);   // Open gripper
      Serial.println("Gripper Open");
    }
    if (incomingData == 'F') {
      servo5.write(90);  // Close gripper
      Serial.println("Gripper Closed");
    }
  }
}
