#include "Kocoafab_SmartMobility.h"

Kocoafab_SmartMobility::Kocoafab_SmartMobility() {
}

bool Kocoafab_SmartMobility::begin() {
	AFMS = Adafruit_MotorShield();

	motor1 = AFMS.getMotor(1);
	motor2 = AFMS.getMotor(2);
	motor3 = AFMS.getMotor(3);
	motor4 = AFMS.getMotor(4);

	return AFMS.begin();
}


void Kocoafab_SmartMobility::setSpeed(uint16_t speed) {
	if(speed > 500){
		speed = 500;
	}
	
	motor1->setSpeed(speed);
	motor2->setSpeed(speed);
	motor3->setSpeed(speed);
	motor4->setSpeed(speed);
}


void Kocoafab_SmartMobility::setSpeed(uint8_t id, uint16_t speed) {
	if(speed > 200){
		speed = 300;
	}
	
	if(id == 1){
		motor1->setSpeed(speed);	
	}else if(id == 2){
		motor2->setSpeed(speed);
	}else if(id == 3){
		motor3->setSpeed(speed);  
	}else if(id == 4){
		motor4->setSpeed(speed);  
	}
}

// Kocoafab_SmartMobility move function
void Kocoafab_SmartMobility::moveF(){
	motor1->run(FORWARD);
	motor2->run(FORWARD);
	motor3->run(FORWARD);
	motor4->run(FORWARD);
}

void Kocoafab_SmartMobility::moveF(uint16_t length){
	motor1->run(FORWARD);
	motor2->run(FORWARD);
	motor3->run(FORWARD);
	motor4->run(FORWARD);
	delay(length);
	motor1->run(RELEASE);
	motor2->run(RELEASE);
	motor3->run(RELEASE);
	motor4->run(RELEASE);	
}

void Kocoafab_SmartMobility::moveL(){
	motor1->run(BACKWARD);
	motor2->run(FORWARD);
	motor3->run(BACKWARD);
	motor4->run(FORWARD);
}

void Kocoafab_SmartMobility::moveL(uint16_t length){
	motor1->run(BACKWARD);
	motor2->run(FORWARD);
	motor3->run(BACKWARD);
	motor4->run(FORWARD);
	delay(length);
	motor1->run(RELEASE);
	motor2->run(RELEASE);
	motor3->run(RELEASE);
	motor4->run(RELEASE);	
}

void Kocoafab_SmartMobility::moveR(){
	motor1->run(FORWARD);
	motor2->run(BACKWARD);
	motor3->run(FORWARD);
	motor4->run(BACKWARD);
}

void Kocoafab_SmartMobility::moveR(uint16_t length){
	motor1->run(FORWARD);
	motor2->run(BACKWARD);
	motor3->run(FORWARD);
	motor4->run(BACKWARD);
	delay(length);
	motor1->run(RELEASE);
	motor2->run(RELEASE);
	motor3->run(RELEASE);
	motor4->run(RELEASE);	
}

void Kocoafab_SmartMobility::moveB(){
	motor1->run(BACKWARD);
	motor2->run(BACKWARD);
	motor3->run(BACKWARD);
	motor4->run(BACKWARD);
}

void Kocoafab_SmartMobility::moveB(uint16_t length){
	motor1->run(BACKWARD);
	motor2->run(BACKWARD);
	motor3->run(BACKWARD);
	motor4->run(BACKWARD);
	delay(length);
	motor1->run(RELEASE);
	motor2->run(RELEASE);
	motor3->run(RELEASE);
	motor4->run(RELEASE);
}

void Kocoafab_SmartMobility::moveLF(){
	motor1->run(RELEASE);
	motor2->run(FORWARD);
	motor3->run(RELEASE);
	motor4->run(FORWARD);
}

void Kocoafab_SmartMobility::moveLF(uint16_t length){
	motor1->run(RELEASE);
	motor2->run(FORWARD);
	motor3->run(RELEASE);
	motor4->run(FORWARD);
	delay(length);
	motor1->run(RELEASE);
	motor2->run(RELEASE);
	motor3->run(RELEASE);
	motor4->run(RELEASE);
}

void Kocoafab_SmartMobility::moveRF(){
	motor1->run(FORWARD);
	motor2->run(RELEASE);
	motor3->run(FORWARD);
	motor4->run(RELEASE);
}

void Kocoafab_SmartMobility::moveRF(uint16_t length){
	motor1->run(FORWARD);
	motor2->run(RELEASE);
	motor3->run(FORWARD);
	motor4->run(RELEASE);
	delay(length);
	motor1->run(RELEASE);
	motor2->run(RELEASE);
	motor3->run(RELEASE);
	motor4->run(RELEASE);	
}

void Kocoafab_SmartMobility::moveLB(){
	motor1->run(BACKWARD);
	motor2->run(RELEASE);
	motor3->run(BACKWARD);
	motor4->run(RELEASE);
}

void Kocoafab_SmartMobility::moveLB(uint16_t length){
	motor1->run(BACKWARD);
	motor2->run(RELEASE);
	motor3->run(BACKWARD);
	motor4->run(RELEASE);
	delay(length);
	motor1->run(RELEASE);
	motor2->run(RELEASE);
	motor3->run(RELEASE);
	motor4->run(RELEASE);	
}

void Kocoafab_SmartMobility::moveRB(){
	motor1->run(RELEASE);
	motor2->run(BACKWARD);
	motor3->run(RELEASE);
	motor4->run(BACKWARD);
}

void Kocoafab_SmartMobility::moveRB(uint16_t length){
	motor1->run(RELEASE);
	motor2->run(BACKWARD);
	motor3->run(RELEASE);
	motor4->run(BACKWARD);
	delay(length);
	motor1->run(RELEASE);
	motor2->run(RELEASE);
	motor3->run(RELEASE);
	motor4->run(RELEASE);
}

void Kocoafab_SmartMobility::stopAll(){
	motor1->run(RELEASE);
	motor2->run(RELEASE);
	motor3->run(RELEASE);
	motor4->run(RELEASE);
}

void Kocoafab_SmartMobility::stopAll(uint16_t length){
	motor1->run(RELEASE);
	motor2->run(RELEASE);
	motor3->run(RELEASE);
	motor4->run(RELEASE);
	delay(length);
}

// 스모키 움직임 함수(단독 명령어)
void Kocoafab_SmartMobility::moveTo(uint8_t cmd){
	if(cmd == 1){
		motor1->run(BACKWARD);
		motor2->run(RELEASE);
		motor3->run(BACKWARD);
		motor4->run(RELEASE);
	}
	else if(cmd == 2){
		motor1->run(BACKWARD);
		motor2->run(BACKWARD);
		motor3->run(BACKWARD);
		motor4->run(BACKWARD);
	}
	else if(cmd == 3){
		motor1->run(RELEASE);
		motor2->run(BACKWARD);
		motor3->run(RELEASE);
		motor4->run(BACKWARD);
	}
	else if(cmd == 4){
		motor1->run(BACKWARD);
		motor2->run(FORWARD);
		motor3->run(BACKWARD);
		motor4->run(FORWARD);
	}
	else if(cmd == 5){
		motor1->run(RELEASE);
		motor2->run(RELEASE);
		motor3->run(RELEASE);
		motor4->run(RELEASE);
	}
	else if(cmd == 6){
		motor1->run(FORWARD);
		motor2->run(BACKWARD);
		motor3->run(FORWARD);
		motor4->run(BACKWARD);
	}
	else if(cmd == 7){
		motor1->run(RELEASE);
		motor2->run(FORWARD);
		motor3->run(RELEASE);
		motor4->run(FORWARD);
	}
	else if(cmd == 8){
		motor1->run(FORWARD);
		motor2->run(FORWARD);
		motor3->run(FORWARD);
		motor4->run(FORWARD);
	}
	else if(cmd == 9){
		motor1->run(FORWARD);
		motor2->run(RELEASE);
		motor3->run(FORWARD);
		motor4->run(RELEASE);
	}
}


// 스모키 움직임 함수(단독 명령어)
void Kocoafab_SmartMobility::moveTo(uint8_t cmd, uint16_t length){
	if(cmd == 1){
		motor1->run(RELEASE);
		motor2->run(FORWARD);
		motor3->run(RELEASE);
		motor4->run(FORWARD);
	}
	else if(cmd == 2){
		motor1->run(BACKWARD);
		motor2->run(BACKWARD);
		motor3->run(BACKWARD);
		motor4->run(BACKWARD);
	}
	else if(cmd == 3){
		motor1->run(FORWARD);
		motor2->run(RELEASE);
		motor3->run(FORWARD);
		motor4->run(RELEASE);
	}
	else if(cmd == 4){
		motor1->run(BACKWARD);
		motor2->run(FORWARD);
		motor3->run(BACKWARD);
		motor4->run(FORWARD);
	}
	else if(cmd == 5){
		motor1->run(RELEASE);
		motor2->run(RELEASE);
		motor3->run(RELEASE);
		motor4->run(RELEASE);
	}
	else if(cmd == 6){
		motor1->run(FORWARD);
		motor2->run(BACKWARD);
		motor3->run(FORWARD);
		motor4->run(BACKWARD);
	}
	else if(cmd == 7){
		motor1->run(BACKWARD);
		motor2->run(RELEASE);
		motor3->run(BACKWARD);
		motor4->run(RELEASE);
	}
	else if(cmd == 8){
		motor1->run(FORWARD);
		motor2->run(FORWARD);
		motor3->run(FORWARD);
		motor4->run(FORWARD);
	}
	else if(cmd == 9){
		motor1->run(RELEASE);
		motor2->run(BACKWARD);
		motor3->run(RELEASE);
		motor4->run(BACKWARD);
	}
	
	delay(length);
	
	motor1->run(RELEASE);
	motor2->run(RELEASE);
	motor3->run(RELEASE);
	motor4->run(RELEASE);
}


// 스모키 움직임 함수(단독 명령어)
void Kocoafab_SmartMobility::setMove(uint8_t cmd){
	if(cmd == 1){
		motor1->run(FORWARD);
		motor2->run(FORWARD);
		motor3->run(FORWARD);
		motor4->run(FORWARD);
	}
	else if(cmd == 2){
		motor1->run(BACKWARD);
		motor2->run(BACKWARD);
		motor3->run(BACKWARD);
		motor4->run(BACKWARD);
	}
	else if(cmd == 3){
		motor1->run(RELEASE);
		motor2->run(RELEASE);
		motor3->run(RELEASE);
		motor4->run(RELEASE);
	}
	else if(cmd == 4){
		motor1->run(BACKWARD);
		motor2->run(FORWARD);
		motor3->run(BACKWARD);
		motor4->run(FORWARD);
	}
	else if(cmd == 5){
		motor1->run(FORWARD);
		motor2->run(BACKWARD);
		motor3->run(FORWARD);
		motor4->run(BACKWARD);
	}
	else if(cmd == 6){
		motor1->run(RELEASE);
		motor2->run(FORWARD);
		motor3->run(RELEASE);
		motor4->run(FORWARD);
	}
	else if(cmd == 7){
		motor1->run(FORWARD);
		motor2->run(RELEASE);
		motor3->run(FORWARD);
		motor4->run(RELEASE);
	}
	else if(cmd == 8){
		motor1->run(BACKWARD);
		motor2->run(RELEASE);
		motor3->run(BACKWARD);
		motor4->run(RELEASE);
	}
	else if(cmd == 9){
		motor1->run(RELEASE);
		motor2->run(BACKWARD);
		motor3->run(RELEASE);
		motor4->run(BACKWARD);
	}
}

// 스모키 움직임 함수(단독 명령어)
void Kocoafab_SmartMobility::setMove(uint8_t cmd, uint16_t length){
	if(cmd == 1){
		motor1->run(FORWARD);
		motor2->run(FORWARD);
		motor3->run(FORWARD);
		motor4->run(FORWARD);
	}
	else if(cmd == 2){
		motor1->run(BACKWARD);
		motor2->run(BACKWARD);
		motor3->run(BACKWARD);
		motor4->run(BACKWARD);
	}
	else if(cmd == 3){
		motor1->run(RELEASE);
		motor2->run(RELEASE);
		motor3->run(RELEASE);
		motor4->run(RELEASE);
	}
	else if(cmd == 4){
		motor1->run(BACKWARD);
		motor2->run(FORWARD);
		motor3->run(BACKWARD);
		motor4->run(FORWARD);
	}
	else if(cmd == 5){
		motor1->run(FORWARD);
		motor2->run(BACKWARD);
		motor3->run(FORWARD);
		motor4->run(BACKWARD);
	}
	else if(cmd == 6){
		motor1->run(RELEASE);
		motor2->run(FORWARD);
		motor3->run(RELEASE);
		motor4->run(FORWARD);
	}
	else if(cmd == 7){
		motor1->run(FORWARD);
		motor2->run(RELEASE);
		motor3->run(FORWARD);
		motor4->run(RELEASE);
	}
	else if(cmd == 8){
		motor1->run(BACKWARD);
		motor2->run(RELEASE);
		motor3->run(BACKWARD);
		motor4->run(RELEASE);
	}
	else if(cmd == 9){
		motor1->run(RELEASE);
		motor2->run(BACKWARD);
		motor3->run(RELEASE);
		motor4->run(BACKWARD);
	}
	
	delay(length);
	
	motor1->run(RELEASE);
	motor2->run(RELEASE);
	motor3->run(RELEASE);
	motor4->run(RELEASE);
}

// 스모키 모터 4개 동시 제어(회전 방향)
void Kocoafab_SmartMobility::setMotor(uint8_t cmd){
	motor1->run(cmd);
	motor2->run(cmd);
	motor3->run(cmd);
	motor4->run(cmd);
}


// 모터 1개 제어(모터 번호, 회전 방향)
void Kocoafab_SmartMobility::setMotor(uint8_t id, uint8_t cmd) {
	if(id == 1){
		motor1->run(cmd);
	}
	else if(id == 2){
		motor2->run(cmd);
	}
	else if(id == 3){
		motor3->run(cmd);
	}
	else if(id == 4){
		motor4->run(cmd);
	}  
}


// CW -> 시계방향(우회전) / CCW -> 반시계방향(좌회전)
void Kocoafab_SmartMobility::rotate(uint8_t dir){
	if(dir == 1){
		motor1->run(BACKWARD);
		motor2->run(BACKWARD);
		motor3->run(FORWARD);
		motor4->run(FORWARD);
	}
	
	else if(dir == 2){
		motor1->run(FORWARD);
		motor2->run(FORWARD);
		motor3->run(BACKWARD);
		motor4->run(BACKWARD);		
	}
}

// CW -> 시계방향(우회전), CCW -> 반시계방향(좌회전) / length 회전 시간(ms) 
void Kocoafab_SmartMobility::rotate(uint8_t dir, uint16_t length){
	if(dir == 1){
		motor1->run(BACKWARD);
		motor2->run(BACKWARD);
		motor3->run(FORWARD);
		motor4->run(FORWARD);
		delay(length);
		motor1->run(RELEASE);
		motor2->run(RELEASE);
		motor3->run(RELEASE);
		motor4->run(RELEASE);
	}
	
	else if(dir == 2){
		motor1->run(FORWARD);
		motor2->run(FORWARD);
		motor3->run(BACKWARD);
		motor4->run(BACKWARD);
		delay(length);
		motor1->run(RELEASE);
		motor2->run(RELEASE);
		motor3->run(RELEASE);
		motor4->run(RELEASE);		
	}
}


// length -> delay 시간 / iter -> 반복 횟수 / dir 1(CW) -> 시계방향, 2(CCW) -> 반시계방향
void Kocoafab_SmartMobility::drawRect(uint16_t length, uint16_t iter, uint8_t dir){
	for(int i = 0; i < iter; i++){
		if(dir == 1){
			motor1->run(FORWARD);
			motor2->run(FORWARD);
			motor3->run(FORWARD);
			motor4->run(FORWARD);
			delay(length);
			
			motor1->run(RELEASE);
			motor2->run(RELEASE);
			motor3->run(RELEASE);
			motor4->run(RELEASE);
			delay(100);			
			
			motor1->run(FORWARD);
			motor2->run(BACKWARD);
			motor3->run(FORWARD);
			motor4->run(BACKWARD);
			delay(length);

			motor1->run(RELEASE);
			motor2->run(RELEASE);
			motor3->run(RELEASE);
			motor4->run(RELEASE);
			delay(100);			
			
			motor1->run(BACKWARD);
			motor2->run(BACKWARD);
			motor3->run(BACKWARD);
			motor4->run(BACKWARD);
			delay(length);
			
			motor1->run(RELEASE);
			motor2->run(RELEASE);
			motor3->run(RELEASE);
			motor4->run(RELEASE);
			delay(100);			
			
			motor1->run(BACKWARD);
			motor2->run(FORWARD);
			motor3->run(BACKWARD);
			motor4->run(FORWARD);
			delay(length);	
		}
		
		else if(dir == 2){
			motor1->run(FORWARD);
			motor2->run(BACKWARD);
			motor3->run(FORWARD);
			motor4->run(BACKWARD);
			delay(length);
			
			motor1->run(RELEASE);
			motor2->run(RELEASE);
			motor3->run(RELEASE);
			motor4->run(RELEASE);
			delay(100);			
			
			motor1->run(FORWARD);
			motor2->run(FORWARD);
			motor3->run(FORWARD);
			motor4->run(FORWARD);
			delay(length);
			
			motor1->run(RELEASE);
			motor2->run(RELEASE);
			motor3->run(RELEASE);
			motor4->run(RELEASE);
			delay(100);			
			
			motor1->run(BACKWARD);
			motor2->run(FORWARD);
			motor3->run(BACKWARD);
			motor4->run(FORWARD);
			delay(length);
			
			motor1->run(RELEASE);
			motor2->run(RELEASE);
			motor3->run(RELEASE);
			motor4->run(RELEASE);
			delay(100);			
			
			motor1->run(BACKWARD);
			motor2->run(BACKWARD);
			motor3->run(BACKWARD);
			motor4->run(BACKWARD);
			delay(length);	
		}
	}
	
	motor1->run(RELEASE);
	motor2->run(RELEASE);
	motor3->run(RELEASE);
	motor4->run(RELEASE);
}
	


// length -> delay 시간 / iter -> 반복 횟수 / dir 1(CW) -> 시계방향, 2(CCW) -> 반시계방향
void Kocoafab_SmartMobility::drawTriangle(uint16_t length, uint16_t iter, uint8_t dir){
	for(int i = 0; i < iter; i++){
		if(dir == 1){
			motor1->run(FORWARD);
			motor2->run(RELEASE);
			motor3->run(FORWARD);
			motor4->run(RELEASE);
			delay(length);
			
			motor1->run(RELEASE);
			motor2->run(RELEASE);
			motor3->run(RELEASE);
			motor4->run(RELEASE);
			delay(100);
			
			motor1->run(RELEASE);
			motor2->run(BACKWARD);
			motor3->run(RELEASE);
			motor4->run(BACKWARD);
			delay(length);
			
			motor1->run(RELEASE);
			motor2->run(RELEASE);
			motor3->run(RELEASE);
			motor4->run(RELEASE);
			delay(100);
			
			motor1->run(BACKWARD);
			motor2->run(FORWARD);
			motor3->run(BACKWARD);
			motor4->run(FORWARD);
			delay(length * 1.1);	
		}
		
		else if(dir == 2){
			motor1->run(FORWARD);
			motor2->run(BACKWARD);
			motor3->run(FORWARD);
			motor4->run(BACKWARD);
			delay(length);
			
			motor1->run(RELEASE);
			motor2->run(RELEASE);
			motor3->run(RELEASE);
			motor4->run(RELEASE);
			delay(100);
			
			motor1->run(RELEASE);
			motor2->run(FORWARD);
			motor3->run(RELEASE);
			motor4->run(FORWARD);
			delay(length);
			
			motor1->run(RELEASE);
			motor2->run(RELEASE);
			motor3->run(RELEASE);
			motor4->run(RELEASE);
			delay(100);			
			
			motor1->run(BACKWARD);
			motor2->run(RELEASE);
			motor3->run(BACKWARD);
			motor4->run(RELEASE);
			delay(length * 1.1);
		}
	}
	
	motor1->run(RELEASE);
	motor2->run(RELEASE);
	motor3->run(RELEASE);
	motor4->run(RELEASE);
}


void Kocoafab_SmartMobility::setUltrasonic(uint8_t t, uint8_t e){
	trig = t;
	echo = e;
	pinMode(trig, OUTPUT);
	pinMode(echo, INPUT);
}

float Kocoafab_SmartMobility::getDistance(){
	digitalWrite(trig, LOW);
	digitalWrite(echo, LOW);
	delayMicroseconds(2);
	digitalWrite(trig, HIGH);
	delayMicroseconds(10);
	digitalWrite(trig, LOW);

	unsigned long duration = pulseIn(echo, HIGH);
	float dis = duration / 29.0 / 2.0;
	
	return dis;
}
