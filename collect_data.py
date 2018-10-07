import board
import busio
import adafruit_bno055
import time
import numpy as np

i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_bno055.BNO055(i2c)

i = 0
header = "time_ms\ttemp_c\taccel_ms\tmag_uT\tgyro_degs\t\euler_deg\tquaternion\tlin_accel_ms\tgravity_ms\n"
while True:
    # print('Temperature: {} degrees C'.format(sensor.temperature))
    # print('Accelerometer (m/s^2): {}'.format(sensor.accelerometer))
    # print('Magnetometer (microteslas): {}'.format(sensor.magnetometer))
    # print('Gyroscope (deg/sec): {}'.format(sensor.gyroscope))
    # print('Euler angle: {}'.format(sensor.euler))
    # print('Quaternion: {}'.format(sensor.quaternion))
    # print('Linear acceleration (m/s^2): {}'.format(sensor.linear_acceleration))
    # print('Gravity (m/s^2): {}'.format(sensor.gravity))

    time.sleep(100)
    file_name = "data" + i + ".csv"
    input("Press Enter to continue...")
