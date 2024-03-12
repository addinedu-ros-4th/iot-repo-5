#include <Wire.h>
#include "./Addy_SmartMobility.h"
#include <SoftwareSerial.h>

Addy_SmartMobility amr = Addy_SmartMobility();
// SoftwareSerial BTSerial(4, 5);

const int trigPinFront = 2;  // 앞
const int echoPinFront = 3;

const int trigPinRight = 4;  // 우
const int echoPinRight = 5;

const int trigPinBack = 6;  // 뒤
const int echoPinBack = 7;

const int trigPinLeft = 8;  // 좌
const int echoPinLeft = 9;

int gyro_x, gyro_y, gyro_z;
long gyro_x_cal, gyro_y_cal, gyro_z_cal;
boolean set_gyro_angles;

long acc_x, acc_y, acc_z, acc_total_vector;
float angle_roll_acc, angle_pitch_acc;

float angle_pitch, angle_roll;
int angle_pitch_buffer, angle_roll_buffer;
float angle_pitch_output, angle_roll_output;

float target = 0;
float error = 0;
float integral = 0;
float derivative = 0;
float last_error = 0;

float Kp = 11;
float Ki = 0.09;
float Kd = 10;

int speed = 160;

float angle = 0;

long loop_timer;
int temp;
int state = 0;

// 회피할 거리 (센티미터)
const int avoidanceDistance = 10;

void setup() {
  pinMode(trigPinFront, OUTPUT);
  pinMode(echoPinFront, INPUT);
  pinMode(trigPinBack, OUTPUT);
  pinMode(echoPinBack, INPUT);
  pinMode(trigPinLeft, OUTPUT);
  pinMode(echoPinLeft, INPUT);
  pinMode(trigPinRight, OUTPUT);
  pinMode(echoPinRight, INPUT);

  if (!amr.begin()) {
    Serial.println("모터 쉴드 연결을 다시 확인해주세요.");
    while (1)
      ;
  }
  setup_mpu_6050_registers(); 
  for (int cal_int = 0; cal_int < 1000 ; cal_int ++){                  
    read_mpu_6050_data(); 
    //Add the gyro x offset to the gyro_x_cal variable                                            
    gyro_x_cal += gyro_x;
    //Add the gyro y offset to the gyro_y_cal variable                                              
    gyro_y_cal += gyro_y; 
    //Add the gyro z offset to the gyro_z_cal variable                                             
    gyro_z_cal += gyro_z; 
    //Delay 3us to have 250Hz for-loop                                             
    delay(3);
  }         
 // Divide all results by 1000 to get average offset
  gyro_x_cal /= 1000;                                                 
  gyro_y_cal /= 1000;                                                 
  gyro_z_cal /= 1000;


  Serial.begin(9600);

  loop_timer = micros();                                               


}


float getDistance(int trigPin, int echoPin) {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  long duration = pulseIn(echoPin, HIGH);
  float distance = duration * 0.034 / 2;

  return distance;
}
int16_t offset[3] = {32, 15, -12};

float get_Z() {
 // Get data from MPU-6050
  read_mpu_6050_data();
     
  //Subtract the offset values from the raw gyro values
  gyro_x -= gyro_x_cal;                                                
  gyro_y -= gyro_y_cal;                                                
  gyro_z -= gyro_z_cal;                                                
         
  //Gyro angle calculations . Note 0.0000611 = 1 / (250Hz x 65.5)
  
  //Calculate the traveled pitch angle and add this to the angle_pitch variable
  angle_pitch += gyro_x * 0.0000611;  
  //Calculate the traveled roll angle and add this to the angle_roll variable
  //0.000001066 = 0.0000611 * (3.142(PI) / 180degr) The Arduino sin function is in radians                                
  angle_roll += gyro_y * 0.0000611; 
                                     
  //If the IMU has yawed transfer the roll angle to the pitch angle
  angle_pitch += angle_roll * sin(gyro_z * 0.000001066);
  //If the IMU has yawed transfer the pitch angle to the roll angle               
  angle_roll -= angle_pitch * sin(gyro_z * 0.000001066);               
  
  //Accelerometer angle calculations
  
  //Calculate the total accelerometer vector
  acc_total_vector = sqrt((acc_x*acc_x)+(acc_y*acc_y)+(acc_z*acc_z)); 
   
  //57.296 = 1 / (3.142 / 180) The Arduino asin function is in radians
  //Calculate the pitch angle
  angle_pitch_acc = asin((float)acc_y/acc_total_vector)* 57.296; 
  //Calculate the roll angle      
  angle_roll_acc = asin((float)acc_x/acc_total_vector)* -57.296;       
  
  //Accelerometer calibration value for pitch
  angle_pitch_acc -= 0.0;
  //Accelerometer calibration value for roll                                              
  angle_roll_acc -= 0.0;                                               

  if(set_gyro_angles){ 
  
  //If the IMU has been running 
  //Correct the drift of the gyro pitch angle with the accelerometer pitch angle                      
    angle_pitch = angle_pitch * 0.9996 + angle_pitch_acc * 0.0004; 
    //Correct the drift of the gyro roll angle with the accelerometer roll angle    
    angle_roll = angle_roll * 0.9996 + angle_roll_acc * 0.0004;        
  }
  else{ 
    //IMU has just started  
    //Set the gyro pitch angle equal to the accelerometer pitch angle                                                           
    angle_pitch = angle_pitch_acc;
    //Set the gyro roll angle equal to the accelerometer roll angle                                       
    angle_roll = angle_roll_acc;
    //Set the IMU started flag                                       
    set_gyro_angles = true;                                            
  }
  
  //To dampen the pitch and roll angles a complementary filter is used
  //Take 90% of the output pitch value and add 10% of the raw pitch value
  angle_pitch_output = angle_pitch_output * 0.9 + angle_pitch * 0.1; 
  //Take 90% of the output roll value and add 10% of the raw roll value 
  angle_roll_output = angle_roll_output * 0.9 + angle_roll * 0.1; 
  //Wait until the loop_timer reaches 4000us (250Hz) before starting the next loop  
  //-----------------done with mpu6050 calibration--------------------------------------// 
  error = target - angle_pitch_output;// proportional
  integral = integral + error; //integral
  derivative = error - last_error; //derivative

  angle = (error * Kp) + (integral * Ki) + (derivative * Kd);
  Serial.println(angle_pitch_output);
  return angle, angle_pitch_output;
}


void resetAngle() {
  Serial.println("Resetting Angle!");
  read_mpu_6050_data();
}

void correction_F() {
  
  if (z_ang > 0){
    amr.setSpeed(2, speed + angle);
    amr.setSpeed(3, speed - angle);
  }
  else if(z_ang < 0) {
    amr.setSpeed(2, speed - angle);
    amr.setSpeed(3, speed + angle);
  }
  else {
    amr.setSpeed(2, speed);
    amr.setSpeed(3, speed);
  }
}

void correction_S() {  
  if (z_ang > 0){
    amr.setSpeed(4, speed + angle);
    amr.setSpeed(1, speed - angle);
  }
  else if(z_ang < 0) {
    amr.setSpeed(4, speed - angle);
    amr.setSpeed(1, speed + angle);
  }
  else {
    amr.setSpeed(4, speed);
    amr.setSpeed(1, speed);
  }
}

void loop() {
  float angle, z_ang = get_Z();

  float distanceFront = getDistance(trigPinFront, echoPinFront);
  float distanceBack = getDistance(trigPinBack, echoPinBack);
  float distanceLeft = getDistance(trigPinLeft, echoPinLeft);
  float distanceRight = getDistance(trigPinRight, echoPinRight);

  enum AvoidanceState {
    NO_OBSTACLE,
    AVOIDING_BACK,
    AVOIDING_FRONT,
    AVOIDING_LEFT,
    AVOIDING_RIGHT,
    STOPPED
  };

  AvoidanceState avoidanceState = NO_OBSTACLE;

  switch (avoidanceState) {
    case NO_OBSTACLE:
      // 장애물이 있는지 확인
      if (distanceFront <= avoidanceDistance) {
        avoidanceState = AVOIDING_BACK;
      } else if (distanceBack <= avoidanceDistance) {
        avoidanceState = AVOIDING_FRONT;
      } else if (distanceRight <= avoidanceDistance) {
        avoidanceState = AVOIDING_LEFT;
      } else if (distanceLeft <= avoidanceDistance) {
        avoidanceState = AVOIDING_RIGHT;
      } else {
        correction_F();
        amr.moveF(200);
      }

    case AVOIDING_BACK:
      if (distanceFront < avoidanceDistance) {
        amr.stopAll();

        if (distanceRight > distanceLeft && distanceRight > avoidanceDistance) {
          amr.rotate(1, 600); // CW
          resetAngle();
          break;
        }
        else if (distanceLeft > distanceRight && distanceLeft > avoidanceDistance){
          amr.rotate(2, 600); // CCW
          resetAngle();
          break;
        }
        else {
          amr.moveB(300);
          break;
        }
        break;
      }

    case AVOIDING_FRONT:
      if (distanceBack < avoidanceDistance) {
        correction_F();
        amr.moveF(300);
        // break;
      }

    case AVOIDING_LEFT:
      if (distanceRight < avoidanceDistance) {
        correction_S();
        amr.moveL(300);
        // break;
      }

    case AVOIDING_RIGHT:
      if (distanceLeft < avoidanceDistance) {
        correction_S();
        amr.moveR(300);
        // break;
      }
  }

  Serial.print("Front: ");
  Serial.print(distanceFront);
  Serial.print(" cm   Back: ");
  Serial.print(distanceBack);
  Serial.print(" cm   Left: ");
  Serial.print(distanceLeft);
  Serial.print(" cm   Right: ");
  Serial.print(distanceRight);
  Serial.println(" cm");
}

void setup_mpu_6050_registers(){

  //Activate the MPU-6050
  
  //Start communicating with the MPU-6050
  Wire.beginTransmission(0x68); 
  //Send the requested starting register                                       
  Wire.write(0x6B);  
  //Set the requested starting register                                                  
  Wire.write(0x00);
  //End the transmission                                                    
  Wire.endTransmission(); 
                                              
  //Configure the accelerometer (+/-8g)
  
  //Start communicating with the MPU-6050
  Wire.beginTransmission(0x68); 
  //Send the requested starting register                                       
  Wire.write(0x1C);   
  //Set the requested starting register                                                 
  Wire.write(0x10); 
  //End the transmission                                                   
  Wire.endTransmission(); 
                                              
  //Configure the gyro (500dps full scale)
  
  //Start communicating with the MPU-6050
  Wire.beginTransmission(0x68);
  //Send the requested starting register                                        
  Wire.write(0x1B);
  //Set the requested starting register                                                    
  Wire.write(0x08); 
  //End the transmission                                                  
  Wire.endTransmission(); 
                                              
}

void read_mpu_6050_data(){ 

  //Read the raw gyro and accelerometer data

  //Start communicating with the MPU-6050                                          
  Wire.beginTransmission(0x68);  
  //Send the requested starting register                                      
  Wire.write(0x3B);
  //End the transmission                                                    
  Wire.endTransmission(); 
  //Request 14 bytes from the MPU-6050                                  
  Wire.requestFrom(0x68,14);    
  //Wait until all the bytes are received                                       
  while(Wire.available() < 14);
  
  //Following statements left shift 8 bits, then bitwise OR.  
  //Turns two 8-bit values into one 16-bit value                                       
  acc_x = Wire.read()<<8|Wire.read();                                  
  acc_y = Wire.read()<<8|Wire.read();                                  
  acc_z = Wire.read()<<8|Wire.read();                                  
  temp = Wire.read()<<8|Wire.read();                                   
  gyro_x = Wire.read()<<8|Wire.read();                                 
  gyro_y = Wire.read()<<8|Wire.read();                                 
  gyro_z = Wire.read()<<8|Wire.read(); 
                                 
}
