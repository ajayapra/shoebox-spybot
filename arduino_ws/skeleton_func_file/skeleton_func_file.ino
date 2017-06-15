#include <Servo.h>

//Servo stuff
 Servo myservo;
 int servo_ang;
 int servo_pin = 3;

//H bridge stuff
 //These two pins provide the PWM inputs
 int enA = 5;
 int enB = 9;
 //These pins decide which H bridge switches get enabled
 int in1 = 6; //right
 int in2 = 7; //right
 int in3 = 8; //left
 int in4 = A3; //left

void setup() {
  // put your setup code here, to run once:
  myservo.attach(servo_pin);
  pinMode(enA,OUTPUT);
  pinMode(enB,OUTPUT);
  pinMode(in1,OUTPUT); 
  pinMode(in2,OUTPUT);
  pinMode(in3,OUTPUT); 
  pinMode(in4,OUTPUT); 

}

void updateMot(int left, int right) {
  //updateMot function. Handles two integer inputs that are the speeds of motor A and motor B between -100 and 100
  //Set left and right to the same value to move forward
  // -100 <= (left/right) <= 100
  //Controls the L298N module direction and scales the outputs to be full range
  //init pins above
  if(left<0){ //left side moves rev
    digitalWrite(in3,HIGH);
    digitalWrite(in4,LOW);
  } else { //left side moves fwd
    digitalWrite(in3,LOW);
    digitalWrite(in4,HIGH);
  }
  if(right>0) { //right side moves fwd
    digitalWrite(in1,HIGH);
    digitalWrite(in2,LOW);
  } else { //right side moves rev
    digitalWrite(in1,LOW);
    digitalWrite(in2,HIGH);
  }

  //scale the output to be from 0-255
  left = constrain(abs(left),0,100);
  right = constrain(abs(right),0,100);
  left = map(left,0,100,0,255);
  right = map(right,0,100,0,255);

  //PWM output
  analogWrite(enB,left);
  analogWrite(enA,right);
}

void loop() {
  // put your main code here, to run repeatedly:
  int left_value;
  int right_value;
  left_value = 50;
  right_value = 50;
  updateMot(left_value, right_value);

}
