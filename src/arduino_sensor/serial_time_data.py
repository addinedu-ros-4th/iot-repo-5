import serial
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from datetime import datetime
import threading
import time

# 시리얼 포트 설정
serial_port = '/dev/ttyACM0'  # 아두이노와 연결된 포트로 변경해주세요
baud_rate = 9600

# 데이터 저장을 위한 리스트 초기화
timestamps = []
temperatures = []
humidities = []
co2_levels = []
pm10_levels = []

# 시리얼 포트 열기
ser = serial.Serial(serial_port, baud_rate)

# Danger 메시지 표시 관련 변수
show_danger = False
last_danger_time = None

# AQI 범위 및 레이블
aqi_bins = [0, 50, 100, 250, 500]
aqi_labels = ['Good', 'Moderate', 'Unhealthy', 'Very Unhealthy']

# 데이터 수신 함수
def update_data(frame):
    global timestamps, temperatures, humidities, co2_levels, pm10_levels, show_danger, last_danger_time

    # 시리얼 포트에서 데이터 읽기
    line = ser.readline().decode('utf-8').rstrip()

    # 데이터가 잘못된 형식인 경우 건너뜁니다.
    if not line.startswith("Temperature:"):
        return

    # 데이터를 파싱하여 각 변수에 저장
    data = line.split(",")
    temp = float(data[0].split(":")[1].strip().replace("°C", ""))
    humidity = float(data[1].split(":")[1].strip().replace("%", ""))
    co2 = int(data[2].split(":")[1].strip().replace("ppm", ""))
    pm10 = float(data[3].split(":")[1].strip().replace("ug/m3", ""))
    timestamp = datetime.now()

    # 데이터를 리스트에 추가
    timestamps.append(timestamp)
    temperatures.append(temp)
    humidities.append(humidity)
    co2_levels.append(co2)
    pm10_levels.append(pm10)

    # Danger 메시지 표시 관리
    if pm10 >= 100:
        show_danger = True
        last_danger_time = time.time()
    elif show_danger and time.time() - last_danger_time > 3:
        show_danger = False

    # AQI 계산
    aqi = calculate_aqi(pm10)
    status = get_aqi_status(aqi)

    # 그래프 업데이트
    ax.clear()
    ax.plot(timestamps, temperatures, label='Temperature (°C)')
    ax.plot(timestamps, humidities, label='Humidity (%)')
    ax.plot(timestamps, co2_levels, label='CO2 (ppm)')
    ax.plot(timestamps, pm10_levels, label='PM10 (ug/m3)')
    ax.set_xlabel('Time')
    ax.set_ylabel('Value')
    ax.set_title(f'Sensor Data Over Time - AQI: {aqi}, Status: {status}')
    ax.legend()
    ax.grid(True)
    ax.tick_params(axis='x', rotation=45)

    # Danger 메시지 표시
    if show_danger:
        ax.text(0.5, 0.5, "Danger!!!", horizontalalignment='center', verticalalignment='center', transform=ax.transAxes, fontsize=20, color='red')

# AQI 계산 함수
def calculate_aqi(pm10):
    return ((100 - 51) / (80 - 31)) * (pm10 - 31) + 51

# AQI 상태 가져오기 함수
def get_aqi_status(aqi):
    for i in range(len(aqi_bins)):
        if aqi <= aqi_bins[i]:
            return aqi_labels[i]
    return aqi_labels[-1]  # 최대 범위 이상인 경우

# 그래프 생성
fig, ax = plt.subplots(figsize=(10, 6))

# 애니메이션 생성
ani = FuncAnimation(fig, update_data, interval=1000)

# 그래프 표시
plt.show()
