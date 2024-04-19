# IoT 프로젝트 5조 : 실내 환경 모니터링 모바일 로봇(AdDY)
> **AdDY : Addin-edu Data Yummy**<br>
> **학원 실내 환경 모니터링 모바일 시스템**<br>
## 0. 영상
<div align="center">
  <a href="https://www.youtube.com/watch?v=DpeRxUGIuqw">
      <img src="https://img.youtube.com/vi/DpeRxUGIuqw/maxresdefault.jpg" alt="pinkla b" width="60%" height="60%">
  </a>
</div>

## 1. 프로젝트 개요
  - **주제** : 로봇을 통해 실내 환경 데이터 수집 및 분석하여 쾌적한 환경 조성 솔루션을 사용자(관리자)에게 제안하는 시스템 구현
  - **개발 목표**
    - 하드웨어 제어 및 데이터 수집을 위한 무선 통신 구현
    - 이동형 장치(모바일 로봇)를 통한 환경 센서 데이터 수집 및 데이터 분석을 통한 실내 환경 상태 분석
    - GUI를 활용한 실내 환경 데이터 정보 제공
  - **활용 기술**
    | 구분 | 상세 |
    |------------------|-----------------------------------------------------------------------------------------|
    | 개발 환경| <img src="https://img.shields.io/badge/ubuntu-E95420?style=for-the-badge&logo=ubuntu&logoColor=white"> <img src="https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white"> <img src="https://img.shields.io/badge/c++-00599C?style=for-the-badge&logo=c++&logoColor=white">|
    | 영상처리 | <img src="https://img.shields.io/badge/opencv-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white">|
    | 데이터베이스| <img src="https://img.shields.io/badge/mysql-4479A1?style=for-the-badge&logo=mysql&logoColor=white"> <img src="https://img.shields.io/badge/pandas-150458?style=for-the-badge&logo=pandas&logoColor=white"> <img src="https://img.shields.io/badge/tensorflow-FF6F00?style=for-the-badge&logo=tensorflow&logoColor=white">|
    | GUI| <img src="https://img.shields.io/badge/pyqt5-41CD52?style=for-the-badge&logo=qt&logoColor=white">|
    | 통신| ![image](https://github.com/addinedu-ros-4th/deeplearning-repo-2/assets/87963649/9d587f25-a595-453d-baee-f5f034e5a1cf)|
    | 하드웨어| <img src="https://img.shields.io/badge/arduino uno-00878F?style=for-the-badge&logo=arduino&logoColor=white">|
    | 형상관리 및 협업| <img src="https://img.shields.io/badge/github-181717?style=for-the-badge&logo=github&logoColor=white"> <img src="https://img.shields.io/badge/notion-000000?style=for-the-badge&logo=notion&logoColor=white"> <img src="https://img.shields.io/badge/slack-4A154B?style=for-the-badge&logo=slack&logoColor=white">|
  
## 2. 팀원별 담당 업무 및 프로젝트 진행 일정
![image](https://github.com/addinedu-ros-4th/iot-repo-5/assets/87963649/5a746d43-1b51-4b21-9801-96200485789c)

## 3. 시스템 구성
- **시스템 구성도**
  ![flowchart-main](https://github.com/addinedu-ros-4th/iot-repo-5/assets/87963649/23894484-271a-4d6d-a7af-9fc171900d24)<br>
- **주행 시나리오**
  ![image](https://github.com/addinedu-ros-4th/iot-repo-5/assets/87963649/c3e00510-0b32-4825-a72e-83c889cfdefc)<br>
  > 각 Place의 바닥에 부착된 QR 마커를 인식하여 사전 정의된 제어 값에 따라 로봇이 주행하며,
  > 각 구역의 환경 데이터 수집 및 분석 수행
  - Place1 : 상담실
  - Place2 : 로비
  - Place3 : 회의실
  - Place4 : 강의장 입구
  - Place5 : 강의장 Front
  - Place6 : 강의장 End
  
- **GUI 구성**
  ![image](https://github.com/addinedu-ros-4th/iot-repo-5/assets/87963649/ef820a8d-195a-47ee-9c8f-226c11b75bbf)

- **모바일 로봇 HW 구성**
  ![image](https://github.com/addinedu-ros-4th/iot-repo-5/assets/87963649/a13d8c18-bb16-4958-9587-9722a1f84fdf)

## 4. 기능 리스트
![image](https://github.com/addinedu-ros-4th/iot-repo-5/assets/87963649/db39d910-8e7f-4a67-8933-2ebf751bced5)

## 5. 개선 사항
1. 배선 및 연결 불안정성
2. 다수이 I/O 장치로 인한 전력 부족 현상으로 정상 동작하지 않는 문제 개선
3. 각 구역 센서 데이터 수집과 실내 주행 관련 기능 구현
