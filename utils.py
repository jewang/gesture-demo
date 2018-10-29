import numpy as np
from Adafruit_BNO055 import BNO055


QUATERNION_SCALE = (1.0 / (1<<14))

def get_features(series, generate_feature_names=False):
  if generate_feature_names:
    return ['max', 'min', 'range', 'mean', 'std', 'var']
  features = []
  features.append(max(series))
  features.append(min(series))
  features.append(max(series) - min(series))
  features.append(series.mean())
  features.append(series.std())
  features.append(series.var())
  return features


def get_all_features(trace, generate_feature_names=False):
  features = []
  trace["accel"] = np.linalg.norm(
    (trace["accel_ms2_x"], trace["accel_ms2_y"], trace["accel_ms2_z"]))
  trace["gyro"] = np.linalg.norm(
    (trace['gyro_degs_x'], trace[u'gyro_degs_y'], trace[u'gyro_degs_z']))

  for sensor in ['accel', 'gyro', 'gyro_degs_y', 'gyro_degs_z']:
    features_temp = get_features(trace[sensor], generate_feature_names)
    if generate_feature_names:
      features.extend([x + '_' + sensor for x in features_temp])
    else:
      features.extend(features_temp)
  return features

def get_sensor_headers():
  header = []
  for sensor in ["accel_ms2", "mag_uT", "gyro_degs", "euler_deg", "quaternion",
                 "lin_accel_ms2", "gravity_ms2"]:
    if sensor is "quaternion":
      header.append(sensor + "_w")
    header.append(sensor + "_x")
    header.append(sensor + "_y")
    header.append(sensor + "_z")
  return header

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