import re
import serial
import csv
import time

port = '/dev/ttyACM0' 
baudrate = 9600  

arduino = serial.Serial(port, baudrate, timeout=1)
time.sleep(2)

csv_filename = '/home/kkyu/amr_ws/DL/IoT_Project/environment.csv'
with open(csv_filename, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Time', 'Temperature (°C)', 'Humidity (%)'])

try:
    while True:
        data = arduino.readline().decode().strip()

        if data:
            print("Received data:", data)
            # 정규 표현식을 사용하여 온도와 습도 추출
            match = re.search(r'Temperature: ([\d.]+)°C , Humidity: ([\d.]+)%', data)
            if match:
                temperature = match.group(1)
                humidity = match.group(2)
                # CSV 파일에 추가
                with open(csv_filename, mode='a', newline='') as file:
                    writer = csv.writer(file)
                    # 현재 시간을 추가하여 데이터 저장
                    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
                    writer.writerow([timestamp, temperature, humidity])

        time.sleep(0.5) 

except KeyboardInterrupt:
    arduino.close()
