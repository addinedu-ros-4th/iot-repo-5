import serial
import matplotlib.pyplot as plt
import koreanize_matplotlib
from matplotlib.animation import FuncAnimation
from datetime import datetime
import threading
import time

serial_port = '/dev/ttyACM0'  
baud_rate = 9600

timestamps = []
temperatures = []
humidities = []
co2_levels = []
pm10_levels = []

ser = serial.Serial(serial_port, baud_rate)

show_danger = False
last_danger_time = None

show_ventilation = False
last_ventilation_time = None

show_dry_air_message = False
last_dry_air_time = None

aqi_bins = [0, 50, 100, 250, 500]
aqi_labels = ['Good', 'Moderate', 'Unhealthy', 'Very Unhealthy']


def update_data(frame):
    global timestamps, temperatures, humidities, co2_levels, pm10_levels, show_danger, last_danger_time, show_ventilation, last_ventilation_time, show_dry_air_message, last_dry_air_time

    try:
        line = ser.readline().decode('utf-8').rstrip()

    except UnicodeDecodeError:
        print("UnicodeDecodeError: Unable to decode the received data.")
        return
    
    if not line.startswith("Temperature:"):
        return

    try:
        data = line.split(",")
        if len(data) < 2:
            print("Insufficient data. Skipping line.")
            return
        
        temp = float(data[0].split(":")[1].strip().replace("°C", ""))
        humidity = float(data[1].split(":")[1].strip().replace("%", ""))
        co2 = float(data[2].split(":")[1].strip().replace("ppm", ""))
        pm10 = float(data[3].split(":")[1].strip().split()[0]) 
        timestamp = datetime.now()

        timestamps.append(timestamp)
        temperatures.append(temp)
        humidities.append(humidity)
        co2_levels.append(co2)
        pm10_levels.append(pm10)
    
        # Danger 메시지 표시 관리
        if show_danger and time.time() - last_danger_time > 3:
            show_danger = False

        # 환기 필요 메시지 표시 관리
        if co2 > 1000:
            show_ventilation = True
            last_ventilation_time = time.time()
        elif show_ventilation and time.time() - last_ventilation_time > 3:
            show_ventilation = False

        # 건조한 공기 메시지 표시 관리
        if humidity <= 35:
            show_dry_air_message = True
            last_dry_air_time = time.time()
        elif show_dry_air_message and time.time() - last_dry_air_time > 5:
            show_dry_air_message = False

        aqi = calculate_aqi(pm10)
        status, color = get_aqi_status(aqi)

        ax.clear()
        ax.plot(timestamps, temperatures, label='Temperature (°C)')
        ax.plot(timestamps, humidities, label='Humidity (%)')
        ax.plot(timestamps, co2_levels, label='CO2 (ppm)')
        ax.plot(timestamps, pm10_levels, label='PM10 (ug/m3)')
        ax.fill_between(timestamps, [pm10 - 10 for pm10 in pm10_levels], [pm10 + 10 for pm10 in pm10_levels], color='gray', alpha=0.5)  # Error bands for PM10 levels
        ax.set_xlabel('Time', fontweight='bold', fontsize='12')
        ax.set_ylabel('Value', fontweight='bold', fontsize='12')
        ax.set_title('Sensor Data Over Time', fontweight='bold', fontsize='18')
        ax.set_facecolor('ivory')

        plt.text(0.03, 1.025, 'AQI : ', horizontalalignment='center', verticalalignment='center', transform=ax.transAxes, fontweight='bold', fontsize=12)
        plt.text(0.15, 1.025, f'{aqi} ({status})', horizontalalignment='center', verticalalignment='center', transform=ax.transAxes, fontweight='bold', fontsize=12, color=color)


        ax.axhspan(300, 400, color='pink', alpha=0.5)  
        fig.legend(loc='upper right', bbox_to_anchor=(0.91, 1.00))  
        ax.grid(True, linestyle='--', linewidth=0.5, color='rosybrown')
        ax.tick_params(axis='x', rotation=45)

        # 주의 및 위험 메시지 표시
        if show_danger:
            ax.text(0.5, 0.5, "주의: 미세먼지 농도가 높습니다.", horizontalalignment='center', verticalalignment='center', transform=ax.transAxes, fontsize=12, color='orange')
        elif show_ventilation:
            ax.text(0.5, 0.5, "환기 필요: CO2 농도가 높습니다!", horizontalalignment='center', verticalalignment='center', transform=ax.transAxes, fontsize=12, color='blue')
        elif show_dry_air_message:
            ax.text(0.5, 0.95, "공기가 건조합니다!", horizontalalignment='center', verticalalignment='center', transform=ax.transAxes, fontsize=12, color='green')

    except ValueError as e:
        print("Error parsing data:", e)

    except IndexError:
        print("Error parsing data: Index out of range.")
        return
    
# AQI 계산 함수
def calculate_aqi(pm10):
    return round(((100 - 51) / (80 - 31)) * (pm10 - 31) + 51, 2) 

def get_aqi_status(aqi):
    if aqi <= 50:
        return 'Good', 'blue'  # Good
    elif aqi <= 100:
        return 'Moderate', 'orange'  # Moderate
    elif aqi <= 250:
        return 'Unhealthy', 'red'  # Unhealthy
    else:
        return 'Very Unhealthy', 'purple'  # Very Unhealthy


fig, ax = plt.subplots(figsize=(10, 8))

ani = FuncAnimation(fig, update_data, interval=300)

plt.show()