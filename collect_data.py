import board
import busio
import adafruit_bno055
import time
import datetime
import numpy
import pandas as pd

i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_bno055.BNO055(i2c)

i = 0
header = "time_ms\ttemp_c\taccel_ms\tmag_uT\tgyro_degs\t\euler_deg\tquaternion\tlin_accel_ms\tgravity_ms\n"
data = []

for i in range(10):
  input("Press Enter to continue...")
  start = datetime.datetime.now()
  elapsed_ms = 0
  while elapsed_ms < 5000:
    row = [elapsed_ms, sensor.temperature, sensor.accelerometer,
           sensor.magnetometer,
           sensor.gyroscope, sensor.gyroscope, sensor.euler,
           sensor.quaternion, sensor.linear_acceleration, sensor.gravity]
    data.append(row)
    time.sleep(1 / 60.) # 16ms
    elapsed_ms = (datetime.datetime.now() - start).total_seconds() * 1000

  file_name = "data" + str(i) + ".csv"
  df = pd.DataFrame.from_dict(data)
  df.to_csv(file_name, header=True, index=True, mode='a')

