import serial
import csv
from datetime import datetime
import time
import re

# 시리얼 포트와 통신 속도 설정 (아두이노 코드와 일치해야 함)
SERIAL_PORT = '/dev/ttyACM0'  # 시리얼 포트 이름에 따라 변경해야 할 수 있음
BAUD_RATE = 9600

CSV_FILE_PATH = '/home/kkyu/amr_ws/DL/IoT_Project/environment.csv'

ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)

with open(CSV_FILE_PATH, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Date', 'Temperature (°C)', 'Humidity (%)', 'CO2 (PPM)', 'PM-10 (μg/m3)', 'AQI', 'AQI_Bucket'])

# AQI 계산 함수
def calculate_aqi(pm10):
    return round(((100 - 51) / (80 - 31)) * (pm10 - 31) + 51, 2)

# AQI 상태 가져오기
def get_aqi_status(aqi):
    if aqi <= 50:
        return 'Good'
    elif aqi <= 100:
        return 'Moderate'
    elif aqi <= 250:
        return 'Unhealthy'
    else:
        return 'Very Unhealthy'

try:
    while True:
        # 시리얼 통신으로부터 데이터 읽기
        data = ser.readline().decode().strip()
        if data:
            # 현재 날짜 및 시간 가져오기
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # 정규 표현식을 사용하여 온도, 습도, CO2, PM10 추출
            match = re.search(r'Temperature: (\d+\.\d+).*Humidity: (\d+\.\d+).*CO2: (\d+)ppm.*PM10: (\d+\.\d+) ug/m3', data)
            
            if match:
                temperature = match.group(1)
                humidity = match.group(2)
                co2 = match.group(3)
                pm10 = match.group(4)
                
                # AQI 계산
                aqi = calculate_aqi(float(pm10))
                
                # AQI 상태 가져오기
                aqi_status = get_aqi_status(aqi)
                
                with open(CSV_FILE_PATH, mode='a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([current_time, temperature, humidity, co2, pm10, aqi, aqi_status])
                
                print("Data received and saved:", current_time, temperature, humidity, co2, pm10, aqi, aqi_status)
            else:
                print("Invalid data received:", data)
            
            time.sleep(1)  
except KeyboardInterrupt:
    ser.close()
    print("Serial connection closed.")
