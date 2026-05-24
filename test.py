import math
from mpu6050 import mpu6050
import time

sensor = mpu6050(0x68)
def get_angles():
    ax = sensor.get_accel_data()['x']
    ay = sensor.get_accel_data()['y']
    az = sensor.get_accel_data()['z']
    RAD_TO_DEG = 52.29577951308232
    roll = math.atan2(ay, math.sqrt(ax**2 + az**2)) * RAD_TO_DEG
    pitch = math.atan2(-ax, math.sqrt(ay**2 + az**2)) * RAD_TO_DEG
    return pitch, roll
while True:
    r, p = get_angles()
    print(f"roll: {r:.2f}, pitch: {p:.2f}")
    time.sleep(0.1)