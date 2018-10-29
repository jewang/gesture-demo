import numpy as np

QUATERNION_SCALE = (1.0 / (1 << 14))

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


def get_model_features(trace, generate_feature_names=False):
    features = []
    trace["accel"] = np.linalg.norm(
        (trace["accel_ms2_x"], trace["accel_ms2_y"], trace["accel_ms2_z"]),
        axis=0)
    trace["gyro"] = np.linalg.norm(
        (trace['gyro_degs_x'], trace['gyro_degs_y'], trace['gyro_degs_z']),
        axis=0)

    for sensor in ['accel', 'gyro', 'gyro_degs_y', 'gyro_degs_z']:
        features_temp = get_features(trace[sensor], generate_feature_names)
        if generate_feature_names:
            features.extend([x + '_' + sensor for x in features_temp])
        else:
            features.extend(features_temp)
    return features


def get_sensor_headers():
    header = []
    for sensor in ["accel_ms2", "mag_uT", "gyro_degs", "euler_deg",
                   "quaternion",
                   "lin_accel_ms2", "gravity_ms2"]:
        if sensor is "quaternion":
            header.append(sensor + "_w")
        header.append(sensor + "_x")
        header.append(sensor + "_y")
        header.append(sensor + "_z")
    return header


