#include <Servo.h>
#include <ros.h>
//#include <stdio.h>
#include <geometry_msgs/Twist.h>
#include <std_msgs/Int8.h>

//GLOBAL HANDLES
int left_drive = 0;
int right_drive = 0;

//Servo stuff
 Servo myservo;
 int servo_ang = 90.0;
 int servo_ang_old = servo_ang;
 int servo_pin = 1;

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

void servo_move(const std_msgs::Int8& movement){
  if (movement.data < 0){
    if (servo_ang > 0){
      servo_ang = servo_ang - 1;
    }
    else {
      servo_ang = 0;
    } 
  }
  else if (movement.data > 0){
    if (servo_ang < 180){
      servo_ang = servo_ang + 1;
    }
    else {
      servo_ang = 180;
    } 
  }
  else {
    servo_ang = servo_ang;
  }
}
  

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

ros::Subscriber<geometry_msgs::Twist> drive_sub("turtle1/cmd_vel", drive ); //Define Subscriber
ros::Subscriber<std_msgs::Int8> servo_sub("servo_cmd", servo_move ); //Define Subscriber

void setup() {
  // put your setup code here, to run once:
  pinMode(enA,OUTPUT);
  pinMode(enB,OUTPUT);
  pinMode(in1,OUTPUT); 
  pinMode(in2,OUTPUT);
  pinMode(in3,OUTPUT); 
  pinMode(in4,OUTPUT);
//  myservo.attach(servo_pin);
//  myservo.write(servo_ang);
//  myservo.detach();
  //Serial.begin(9600);
  nh.initNode();
  nh.subscribe(drive_sub);
  nh.subscribe(servo_sub);
}

void updateMot(int left, int right) {
  if (myservo.attached()){
    myservo.detach();
  }
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

  if(servo_ang_old != servo_ang){
    myservo.attach(servo_pin);
    myservo.write(servo_ang);
    myservo.detach();
    servo_ang_old = servo_ang;
  }

}

void loop() {
  updateMot(left_drive, right_drive);
  //Serial.println(debug);
  nh.spinOnce();
  delay(10);

}
