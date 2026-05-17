import os
os.environ['GPIOZERO_PIN_FACTORY'] = 'lgpio'

from gpiozero import Button

class left_servo:
    def __init__(self, pin, pos, state="left"):
        self.pin = pin
        self.pos = pos
        self.state = state

class right_servo:
    def __init__(self, pin, pos, state="right"):
        self.pin = pin
        self.pos = pos
        self.state = state

class limit_switch:
    def __init__(self, pin, set_state=False):
        self.pin = pin
        self.device = Button(pin, pull_up=True, bounce_time=0.05)
        self.set = set_state

    def is_active(self):
        if self.device.is_pressed:
            self.set = True
            return True
        else:
            self.set = False
            return False

    def close_pin(self):
        try:
            self.device.close()
        except:
            pass

class leg:
    def __init__(self, first, second, third, sensor):
        self.first = first
        self.second = second
        self.third = third
        self.sensor = sensor

    def check_floor(self):
        return self.sensor.is_active()

class set_of_legs:
    def __init__(self, high, mid, low):
        self.high = high
        self.mid = mid
        self.low = low