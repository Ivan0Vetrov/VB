import RPi.GPIO as GPIO
import time

sensor_pin = 17  # GPIO пин, к которому подключен датчик Холла
wheel_diameter = 0.5  # Диаметр колеса в метрах
distance = 0  # Пройденная дистанция
prev_time = 0  # Время предыдущего импульса
prev_pulse_count = 0  # Количество импульсов на предыдущем измерении

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

def convert_to_distance(pulse_count):
    # Расчет пройденной дистанции на основе количества импульсов (pulse_count) и диаметра колеса
    distance = pulse_count * (wheel_diameter * 3.14159)  # Расчет пройденной дистанции
    return distance

def get_speed(pulse_count):
    current_time = time.time()  # Текущее время
    time_diff = current_time - prev_time  # Разница во времени с предыдущим измерением
    speed = (pulse_count - prev_pulse_count) / time_diff  # Расчет скорости
    return speed

def update_distance_speed():
    pulse_count = 0
    prev_state = GPIO.input(sensor_pin)
    global distance, prev_time, prev_pulse_count
    
    try:
        while True:
            curr_state = debounce(sensor_pin)
            
            if curr_state != prev_state:
                pulse_count += 1
                prev_state = curr_state
                
                # Обновление пройденной дистанции
                distance = convert_to_distance(pulse_count)
                
                # Обновление скорости
                speed = get_speed(pulse_count)
                
                # Вывод информации
                print("Пройденная дистанция: {} м".format(distance))
                print("Скорость: {} м/с".format(speed))
                
                # Обновление предыдущих значений
                prev_time = time.time()
                prev_pulse_count = pulse_count
            
    except KeyboardInterrupt:
        GPIO.cleanup()

# Инициализация
setup()

try:
    update_distance_speed()
    
except KeyboardInterrupt:
    GPIO.cleanup()
