import RPi.GPIO as GPIO
import time

sensor_pin = 17  # GPIO пин, к которому подключен датчик Холла
wheel_diameter = 0.5  # Диаметр колеса в метрах

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(sensor_pin, GPIO.IN)

def debounce(pin):
    debounce_time = 0.01  # Время задержки для фильтрации дребезга (в секундах)
    prev_state = GPIO.input(pin)
    
    while True:
        curr_state = GPIO.input(pin)
        
        if curr_state != prev_state:
            time.sleep(debounce_time)
            curr_state = GPIO.input(pin)
            
            if curr_state != prev_state:
                return curr_state
            
        prev_state = curr_state

def convert_to_speed(pulse_count, time_interval):
    # Расчет скорости на основе количества импульсов (pulse_count), диаметра колеса и времени (time_interval)
    distance = pulse_count * (wheel_diameter * 3.14159)  # Расчет пройденного расстояния
    speed = distance / time_interval  # Расчет скорости (расстояние / время)
    return speed

def get_speed():
    pulse_count = 0
    prev_state = GPIO.input(sensor_pin)
    start_time = time.time()
    
    try:
        while True:
            curr_state = debounce(sensor_pin)
            
            if curr_state != prev_state:
                pulse_count += 1
                prev_state = curr_state
                
                # Расчет времени, прошедшего с начала измерений
                current_time = time.time()
                time_interval = current_time - start_time
                
                # Избегаем деления на ноль, если время равно нулю
                if time_interval != 0:
                    speed = convert_to_speed(pulse_count, time_interval)
                    return speed
            
    except KeyboardInterrupt:
        GPIO.cleanup()

# Инициализация
setup()

try:
    while True:
        # Получение текущей скорости
        current_speed = get_speed()
        print("Скорость: {} м/с".format(current_speed))
        time.sleep(1)  # Пауза в 1 секунду

except KeyboardInterrupt:
    GPIO.cleanup()
