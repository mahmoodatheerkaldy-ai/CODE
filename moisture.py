import board
import busio
import time
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1115(i2c)
chan = AnalogIn(ads, 0)

# قيم المعايرة الفعلية التي استخرجتها أنت
DRY_VOLT = 2.1839
WET_VOLT = 1.1556

def get_moisture():
    voltage = chan.voltage
    # المعادلة: (قيمة الهواء - القيمة الحالية) / (مدى التغير) * 100
    # نستخدم clamp لضمان بقاء النسبة بين 0 و 100
    percent = ((DRY_VOLT - voltage) / (DRY_VOLT - WET_VOLT)) * 100
    return max(0, min(100, percent))

