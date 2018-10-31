import busio
import time
import datetime
import pandas as pd
from Adafruit_BNO055 import BNO055
import utils
import os
import collections
from sklearn.externals import joblib
import subprocess
import shlex

model = joblib.load('models/167pt_model.joblib')

def play(gesture):
    subprocess.run(shlex.split('omxplayer sounds/' + gesture + '.mp3 -o alsa:hw:1,0'))

def read_sensors(bno):
    vector = bno._read_vector(BNO055.BNO055_ACCEL_DATA_X_LSB_ADDR, 22)
    accel = [s / 100. for s in vector[:3]]
    mag = [s / 16. for s in vector[3:6]]
    gyro = [s / 900. for s in vector[6:9]]
    euler = [s / 16. for s in vector[9:12]]
    quaternion = [s / QUATERNION_SCALE for s in vector[12:16]]
    lin_accel = [s / 100. for s in vector[16:19]]
    gravity = [s / 100. for s in vector[19:22]]

    return accel + mag + gyro + euler + quaternion + lin_accel + gravity

SAMPLE_RATE_HZ = 100
QUATERNION_SCALE = (1.0 / (1 << 14))

CHECK_TIME_INCREMENT_MS = 200
SAMPLE_SIZE_MS = 1500

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

i = 0
header = ["time_ms"] + utils.get_sensor_headers()
data = collections.deque(maxlen=int(SAMPLE_SIZE_MS / 10)) #10 Hz

print('Starting operation')

start = datetime.datetime.now()
elapsed_ms = 0
last_classified = 0
last_classification = "negative_trim"

while True:
  row = [elapsed_ms] + read_sensors(bno)
  data.append(row)

  if elapsed_ms - last_classified >= CHECK_TIME_INCREMENT_MS and len(data) == data.maxlen:
    df = pd.DataFrame(list(data), columns=header)
    features = utils.get_model_features(df)
    prediction = model.predict([features])[0]

    print(int(elapsed_ms), prediction)
    if prediction != 'negative_trim':# and last_classification != prediction:
        print("========================>", prediction)
        play(prediction)
        data.clear()

    last_classified = elapsed_ms
    last_classification = prediction

  elapsed_ms = (datetime.datetime.now() - start).total_seconds() * 1000

  #if elapsed_ms > 10000:
  #  break
