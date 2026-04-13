
class left_servo:
    def __init__(self, pin, pos, state = "left"):
        self.pin = pin
        self.pos = pos
        self.state = state

class right_servo:
    def __init__(self, pin, pos, state = "right"):
        self.pin = pin
        self.pos = pos
        self.state = state

class limit_switch:
    def __init__(self, pin, set = False):
        self.pin = pin
        self.set = set

class leg:
    def __init__(self, first, second, third, sensor):
        self.first = first
        self.second = second
        self.third = third
        self.sensor = sensor

class set_of_legs:
    def __init__(self, high, mid, low):
        self.high = high
        self.mid = mid
        self.low = low

