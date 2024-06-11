import smbus
import time

bus = smbus.SMBus(1)
rtc_address = 0x68

def bcd_to_decimal(bcd):
    return ((bcd // 16) * 10) + (bcd % 16)

def read_rtc():
    rtc_data = bus.read_i2c_block_data(rtc_address, 0, 7)
    seconds = bcd_to_decimal(rtc_data[0] & 0x7F)
    minutes = bcd_to_decimal(rtc_data[1])
    hours = bcd_to_decimal(rtc_data[2] & 0x3F)
    return hours, minutes, seconds

def display_time(hours, minutes, seconds):
    print("Текущее время: {:02d}:{:02d}:{:02d}".format(hours, minutes, seconds))

def calculate_trip_time(start_time):
    current_time = read_rtc()
    trip_time = (
        (current_time[0] - start_time[0]) * 3600 +
        (current_time[1] - start_time[1]) * 60 +
        (current_time[2] - start_time[2])
    )
    return trip_time

# Инициализация модуля RTC
bus.write_byte_data(rtc_address, 0x0E, 0)
bus.write_byte_data(rtc_address, 0x0F, 0)

try:
    # Запись времени начала поездки
    start_time = read_rtc()
    
    while True:
        # Получение текущего времени
        current_time = read_rtc()
        
        # Вывод текущего времени
        display_time(current_time[0], current_time[1], current_time[2])
        
        # Расчет и вывод времени поездки
        trip_time = calculate_trip_time(start_time)
        print("Время поездки: {} сек".format(trip_time))
        
        time.sleep(1)  # Пауза в 1 секунду

except KeyboardInterrupt:
    pass
