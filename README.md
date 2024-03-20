# IoT 프로젝트 5조 : 실내 환경 모니터링 모바일 로봇(AdDY)
<img src="https://img.shields.io/badge/ubuntu-E95420?style=for-the-badge&logo=ubuntu&logoColor=white">

<img src="https://img.shields.io/badge/c++-00599C?style=for-the-badge&logo=c++&logoColor=white"><img src="https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white"><img src="https://img.shields.io/badge/qt-41CD52?style=for-the-badge&logo=qt&logoColor=white"><img src="https://img.shields.io/badge/arduino-00878F?style=for-the-badge&logo=arduino&logoColor=white"><img src="https://img.shields.io/badge/opencv-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white">

<img src="https://img.shields.io/badge/pandas-150458?style=for-the-badge&logo=pandas&logoColor=white"><img src="https://img.shields.io/badge/tensorflow-FF6F00?style=for-the-badge&logo=tensorflow&logoColor=white"><img src="https://img.shields.io/badge/mysql-4479A1?style=for-the-badge&logo=mysql&logoColor=white">

<img src="https://img.shields.io/badge/github-181717?style=for-the-badge&logo=github&logoColor=white"><img src="https://img.shields.io/badge/notion-000000?style=for-the-badge&logo=notion&logoColor=white">

## 1. 프로젝트 개요
> AdDY : Addin-edu Data Yummy
- 주제 : Addin Edu 학원 실내 환경 모니터링 모바일 로봇 시스템
- 설명 : 주행 로봇이 실내 환경 데이터 수집 및 분석을 통해 사용자 또는 관리자에게 쾌적한 환경을 조성하기 위한 솔루션을 제안하는 시스템 구현
  
## 2. 팀원 및 개발 진행 과정
![image](https://github.com/addinedu-ros-4th/iot-repo-5/assets/87963649/5a746d43-1b51-4b21-9801-96200485789c)


## 3. 작품 시스템 구성
- 주행 시나리오

  ![image](https://github.com/addinedu-ros-4th/iot-repo-5/assets/87963649/c3e00510-0b32-4825-a72e-83c889cfdefc)
  
  > 각 Place의 바닥에 부착된 QR 마커를 인식하여 사전 정의된 제어 값에 따라 로봇이 주행하며,
  > 각 구역의 환경 데이터 수집 및 분석 수행
  - Place1 : 상담실
  - Place2 : 로비
  - Place3 : 회의실
  - Place4 : 강의장 입구
  - Place5 : 강의장 Front
  - Place6 : 강의장 End

    
- 시스템 구성도
  ![flowchart-main](https://github.com/addinedu-ros-4th/iot-repo-5/assets/87963649/23894484-271a-4d6d-a7af-9fc171900d24)

  
- GUI 구성
  ![image](https://github.com/addinedu-ros-4th/iot-repo-5/assets/87963649/ef820a8d-195a-47ee-9c8f-226c11b75bbf)

  
- 모바일 로봇 HW 구성
  ![image](https://github.com/addinedu-ros-4th/iot-repo-5/assets/87963649/a13d8c18-bb16-4958-9587-9722a1f84fdf)

  
## 4. 기능 리스트
![image](https://github.com/addinedu-ros-4th/iot-repo-5/assets/87963649/db39d910-8e7f-4a67-8933-2ebf751bced5)

## 5. 시연 영상
[![Video](https://img.youtube.com/vi/DpeRxUGIuqw/maxresdefault.jpg)](https://www.youtube.com/watch?v=DpeRxUGIuqw)

## 6. 개선 필요 사항
1. 배선 상태 및 연결 불안정성 개선
2. 아두이노에 여러 센서가 연결되면서 전력 부족 현상이 발생하여 esp32-cam 모듈이 정상 작동하지 않는 문제 -> 별도 외부 추가 전원을 인가하여 개선 필요
3. 전력 부족 이슈 개선 후, 각 구역 센서 데이터 수집과 실내 주행 관련 추가 개발 필요
