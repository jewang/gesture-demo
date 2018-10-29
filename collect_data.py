import busio
import time
import datetime
import pandas as pd
import os
from Adafruit_BNO055 import BNO055

SAMPLE_RATE_HZ = 100
QUATERNION_SCALE = (1.0 / (1<<14))

bno = BNO055.BNO055(serial_port='/dev/serial0', rst=18)

# Initialize the BNO055 and stop if something went wrong.
if not bno.begin():
  raise RuntimeError('Failed to initialize BNO055! Is the sensor connected?')

# Print system status and self test result.
status, self_test, error = bno.get_system_status()
print('System status: {0}'.format(status))
print('Self test result (0x0F is normal): 0x{0:02X}'.format(self_test))
# Print out an error if system status is in error mode.
if status == 0x01:
  print('System error: {0}'.format(error))
  print('See datasheet section 4.3.59 for the meaning.')

# Print BNO055 software revision and other diagnostic data.
sw, bl, accel, mag, gyro = bno.get_revision()
print('Software version:   {0}'.format(sw))
print('Bootloader version: {0}'.format(bl))
print('Accelerometer ID:   0x{0:02X}'.format(accel))
print('Magnetometer ID:    0x{0:02X}'.format(mag))
print('Gyroscope ID:       0x{0:02X}\n'.format(gyro))

i = 0
header = ["time_ms", "delta_ms"]
for sensor in ["accel_ms2", "mag_uT", "gyro_degs", "euler_deg", "quaternion", "lin_accel_ms2", "gravity_ms2"]:
  if sensor is "quaternion":
    header.append(sensor + "_w")
  header.append(sensor + "_x")
  header.append(sensor + "_y")
  header.append(sensor + "_z")

# TODO: Use python fire =p
filename = input("Name the folder where data will be stored: ")
if not os.path.exists(filename):
  os.mkdir(filename + '/')
starting_index = int(input("What number should we start on?"))

duration_s = float(input("Please input how long should a sensor trace be in seconds (floats OK): "))

# TODO: Add option to delete just recorded trace if it's bad
# TODO: Add option to save notes per recorded trace 
i = starting_index
while True:
  input("Collecting file " + str(i)+ ". Press Enter to continue...")
  start = datetime.datetime.now()
  elapsed_ms = 0
  previous_elapsed_ms = 0

  data = []
  while elapsed_ms < duration_s * 1000:
    # sys, gyro, accel, mag = bno.get_calibration_status()
    vector = bno._read_vector(BNO055.BNO055_ACCEL_DATA_X_LSB_ADDR, 22)

    accel = [s / 100. for s in vector[:3]]
    mag = [s / 16. for s in vector[3:6]]
    gyro = [s / 900. for s in vector[6:9]]
    euler = [s / 16. for s in vector[9:12]]
    quaternion = [s / QUATERNION_SCALE for s in vector[12:16]]
    lin_accel = [s / 100. for s in vector[16:19]]
    gravity = [s / 100. for s in vector[19:22]]

    row = [elapsed_ms, int(elapsed_ms - previous_elapsed_ms)] # heading, roll, pitch, sys, gyro, accel, mag]
    row += accel + mag + gyro + euler + quaternion + lin_accel + gravity

    data.append(row)
    previous_elapsed_ms = elapsed_ms
    elapsed_ms = (datetime.datetime.now() - start).total_seconds() * 1000

  file_name = filename + "/" + filename + '{0:03d}'.format(i) + ".csv"
  df = pd.DataFrame(data, columns = header)
  df.to_csv(file_name, header=True)
  i += 1
