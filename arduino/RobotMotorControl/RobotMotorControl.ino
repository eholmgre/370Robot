/*
 * Motor Controller Driver
 * version 1.1
 * Author: Erik Holmgren <eholmgre@rams.colostate.edu>
 * Date 2017-04-16
 */

 #include <Servo.h>

void updateSpeed(int left, int right);

// Pins for front-left motor
const int MOTOR1PWM = 2; 
const int MOTOR1FWD = 23;
const int MOTOR1RWD = 22;

// Pins for front-right motor
const int MOTOR2PWM = 5;
const int MOTOR2FWD = 28;
const int MOTOR2RWD = 29;

// Pins for rear-left motor
const int MOTOR3PWM = 3;
const int MOTOR3FWD = 25;
const int MOTOR3RWD = 24;

// Pins for rear-right motor
const int MOTOR4PWM = 4;
const int MOTOR4FWD = 26;
const int MOTOR4RWD = 27;

// Pins for servo/sensors
const int SERVOPIN = 9;

// Directions of left and right side motors
bool lft_fwd = true;
bool rht_fwd = true;

// Speed percentages of left and right side
uint8_t lft_spd = 0;
uint8_t rht_spd = 0;

// Sensor Globals
Servo ping_servo;
int servo_angle;
bool sweepDir;
double maxCur;


void setup() {
  Serial.begin(9600);
  Serial.setTimeout(10);
  
  pinMode(MOTOR1PWM, OUTPUT);
  pinMode(MOTOR1FWD, OUTPUT);
  pinMode(MOTOR1RWD, OUTPUT);
  
  pinMode(MOTOR2PWM, OUTPUT);
  pinMode(MOTOR2FWD, OUTPUT);
  pinMode(MOTOR2RWD, OUTPUT);

  pinMode(MOTOR3PWM, OUTPUT);
  pinMode(MOTOR3FWD, OUTPUT);
  pinMode(MOTOR3RWD, OUTPUT);

  pinMode(MOTOR4PWM, OUTPUT);
  pinMode(MOTOR4FWD, OUTPUT);
  pinMode(MOTOR4RWD, OUTPUT);

  updateSpeed(0, 0);

  //ping_servo.attach(SERVOPIN);
  servo_angle = 0;
  
  

}


void loop() {

  /*
  if (millis() % 100 == 0)
  {
    ping_servo.write(servo_angle);
  }
  */

  analogWrite(SERVOPIN, 128);

  double cur = (analogRead(0) - 514) / 10.0;

  if (cur > maxCur)
    maxCur = cur;

  if (millis() % 500 == 0) { // every half second send current, sonar data, sonar angle, and accelaromater data
    Serial.print("Current: ");
    Serial.println(maxCur);
    Serial.flush();
    maxCur = 0;
  }

  if (Serial.available()) {
    int lft_spd_in = Serial.parseInt();
    int rht_spd_in = Serial.parseInt();
    Serial.print("Recieved: ");
    Serial.print(lft_spd_in);
    Serial.print(", ");
    Serial.println(rht_spd_in);
    Serial.flush();

    updateSpeed(lft_spd_in, rht_spd_in);
  }
  
}

void updateSpeed(int left, int right) {
    if (left < 0) {
      lft_fwd = false;
    }
    
    else {
      lft_fwd = true;
    }

    lft_spd = abs(left);

    if (right < 0) {
      rht_fwd = false;
    }
    
    else {
      rht_fwd = true;
    }

    rht_spd = abs(right);
  
  if (lft_spd != 0) {
    digitalWrite(MOTOR1FWD, lft_fwd);
    digitalWrite(MOTOR1RWD, !lft_fwd);

    digitalWrite(MOTOR3FWD, lft_fwd);
    digitalWrite(MOTOR3RWD, !lft_fwd);

    uint8_t motor1_spd = map(lft_spd, 1, 100, 100, 255);
    analogWrite(MOTOR1PWM, motor1_spd);

    uint8_t motor3_spd = map(lft_spd, 1, 100, 100, 255);
    analogWrite(MOTOR3PWM, motor3_spd);
  }
  
  else {
    digitalWrite(MOTOR1FWD, LOW);
    digitalWrite(MOTOR1RWD, LOW);

    digitalWrite(MOTOR3FWD, LOW);
    digitalWrite(MOTOR3RWD, LOW);
    
    analogWrite(MOTOR1PWM, 0);
    analogWrite(MOTOR3PWM, 0);  
  }

  if (rht_spd != 0) {
    digitalWrite(MOTOR2FWD, rht_fwd);
    digitalWrite(MOTOR2RWD, !rht_fwd);

    digitalWrite(MOTOR4FWD, rht_fwd);
    digitalWrite(MOTOR4RWD, !rht_fwd);

    uint8_t motor2_spd = map(rht_spd, 1, 100, 150, 255);
    analogWrite(MOTOR2PWM, motor2_spd);

    uint8_t motor4_spd = map(rht_spd, 1, 100, 150, 255);
    analogWrite(MOTOR4PWM, motor4_spd);
  }
  
  else {
    digitalWrite(MOTOR2FWD, LOW);
    digitalWrite(MOTOR2RWD, LOW);

    digitalWrite(MOTOR4FWD, LOW);
    digitalWrite(MOTOR4RWD, LOW);

    analogWrite(MOTOR2PWM, 0);
    analogWrite(MOTOR4PWM, 0);
  }
}

