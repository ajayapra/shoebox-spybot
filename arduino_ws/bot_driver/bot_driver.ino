#include <Servo.h>
#include <ros.h>
//#include <stdio.h>
#include <geometry_msgs/Twist.h>

//GLOBAL HANDLES
int left_drive = 0;
int right_drive = 0;
char debug[50];

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

ros::NodeHandle nh; //ROS node handle

void drive(const geometry_msgs::Twist& command){
  float fwd = command.linear.x;
  float ang = command.angular.z;
  fwd = fwd*100; //scale to integers
  ang = ang*100;
    if (ang < 0) {//Assume left for now
      ang = -ang;
      left_drive = map(ang, 70, 120, 25, 75);
      right_drive = 0;
    }
    else if (ang > 0) {
      right_drive = map(ang, 70, 120, 25, 75);
      left_drive = 0;
    }
    else {  
       left_drive = map(fwd, -100, 100, -100, 100);
       right_drive = map(fwd, -100, 100, -100, 100);
    }
  //sprintf(debug, "fwd: %f | ang: %f | left %d | right %d", fwd, ang, left_drive, right_drive);
}

ros::Subscriber<geometry_msgs::Twist> sub("turtle1/cmd_vel", drive ); //Define Subscriber

void setup() {
  // put your setup code here, to run once:
  //myservo.attach(servo_pin);
  pinMode(enA,OUTPUT);
  pinMode(enB,OUTPUT);
  pinMode(in1,OUTPUT); 
  pinMode(in2,OUTPUT);
  pinMode(in3,OUTPUT); 
  pinMode(in4,OUTPUT); 
  //Serial.begin(9600);
  nh.initNode();
  nh.subscribe(sub);
}

void updateMot(int left, int right) {
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
  updateMot(left_drive, right_drive);
  //Serial.println(debug);
  nh.spinOnce();
  delay(10);

}
