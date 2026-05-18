import serial
import time
import platform
import tools
import threading as devil

#------------------------------------------------
#define servos..
LHF = tools.left_servo(1, 90)
LHS = tools.left_servo(2, 90)
LHT = tools.left_servo(3, 90)
LMF = tools.left_servo(4, 90)
LMS = tools.left_servo(5, 90)
LMT = tools.left_servo(6, 90)
LLF = tools.left_servo(7, 90)
LLS = tools.left_servo(8, 90)
LLT = tools.left_servo(9, 90)
RHF = tools.right_servo(32, 90)
RHS = tools.right_servo(31, 90)
RHT = tools.right_servo(30, 90)
RMF = tools.right_servo(29, 90)
RMS = tools.right_servo(28, 90)
RMT = tools.right_servo(27, 90)
RLF = tools.right_servo(26, 90)
RLS = tools.right_servo(25, 90)
RLT = tools.right_servo(24, 90)
camera = tools.left_servo(16, 90)
#-------------------------------------------------
#define sensors...
LH = tools.limit_switch(17)
LM = tools.limit_switch(27)
LL = tools.limit_switch(22)
RH = tools.limit_switch(5)
RM = tools.limit_switch(6)
RL = tools.limit_switch(26)
#-------------------------------------------------
#define legs...
left_high = tools.leg(LHF, LHS, LHT, LH)
left_mid = tools.leg(LMF, LMS, LMT, LM)
left_low = tools.leg(LLF, LLS, LLT, LL)
right_high = tools.leg(RHF, RHS, RHT, RH)
right_mid = tools.leg(RMF, RMS, RMT, RM)
right_low = tools.leg(RLF, RLS, RLT, RL)

#-------------------------------------------------
#define sets of legs...
left_set = tools.set_of_legs(left_high, right_mid, left_low)
right_set = tools.set_of_legs(right_high, left_mid, right_low)
#--------------------------------------------------
#define port...
def get_servo_port():
    current_os = platform.system()
    if current_os == "Windows":
        return "COM5"
    return "/dev/ttyACM0"

try:
    port = get_servo_port()
    ser = serial.Serial(port, 9600, timeout=1)
    print(f"✅ Serial Port {port} Opened Successfully.")
except Exception as e:
    print(f"❌ Failed to open port: {e}")
    ser = None
#--------------------------------------------------
#HELPER FUNCTIONS.<><><><><><><><<><><><><><><><><>
#--------------------------------------------------
#fine other leg.
def is_other_leg(leg):
    if leg == left_set:
        return right_set
    return left_set
# --------------------------------------------------
#SERVO LEVEL.<><><><><><><><><><><<><><><><><><><><>
#--------------------------------------------------
#function to move a single servo to a target angle with optional speed control.
def move_servo(servo, target_angle, speed=700):
    if ser is None or not ser.is_open:
        print("⚠️ Serial port is not open!")
        return
    servo.pos = target_angle
    if servo.state == "right":
        target_angle = 180 - target_angle

    pulse = int(500 + (target_angle / 180.0) * 2000)
    
    try:
        command = f"#{servo.pin}P{pulse}S{speed}\r\n"
        
        ser.write(command.encode())
    except Exception as e:
        print(f"❌ Error during transmission: {e}")

def limit_switch_status():
    status = {
        "LH": LH.is_active(),
        "LM": LM.is_active(),
        "LL": LL.is_active(),
        "RH": RH.is_active(),
        "RM": RM.is_active(),
        "RL": RL.is_active()
    }
    return status

def all_sensors_active():
    count = 0
    for sensor in [LH, LM, LL, RH, RM, RL]:
        if sensor.is_active() == True:
            count += 1
    if count == 6:
        return True
    return False

print(f"\n statsus: {limit_switch_status()}\n")
    
#--------------------------------------------------
def default_pos():
    for servo in [LHF, LHS, LHT, LMF, LMS, LMT, LLF, LLS, LLT, RHF, RHS, RHT, RMF, RMS, RMT, RLF, RLS, RLT, camera]:
        move_servo(servo, 90)
        time.sleep(0.05)

#--------------------------------------------------
#LEG LEVEL.<><><><><><><><><><><><><>
#--------------------------------------------------
#use it for one leg at a time.
def move_leg(leg, pos):
    move_servo(leg.second, 150)
    move_servo(leg.third, 170)
    time.sleep(0.3)
    move_servo(leg.first, pos)
    time.sleep(0.1)
    for i in range(0, 100, 5):
        if leg.sensor.is_active() == True:
            break
        move_servo(leg.second, 140 - i)
        move_servo(leg.third, 170 - i)
        time.sleep(0.05)


def move_three_servos(servo1, servo2, servo3, pos):
    move_servo(servo1, pos)
    move_servo(servo2, pos)
    move_servo(servo3, pos)

def move_two_servos(servo1, servo2, d):
    move_servo(servo1, 140 - d)
    move_servo(servo2, 170 - d)

def body_up(set, wight):
    move_servo(set.high.second, set.high.second.pos - wight)
    move_servo(set.high.third, set.high.third.pos - wight)
    move_servo(set.mid.second, set.mid.second.pos - wight)
    move_servo(set.mid.third, set.mid.third.pos - wight)
    move_servo(set.low.second, set.low.second.pos - wight)
    move_servo(set.low.third, set.low.third.pos - wight)

def x_clokwise(set, pos):
    move_servo(set.high.first, pos)
    move_servo(set.mid.first, 180 - pos)
    move_servo(set.low.first, pos)
def x_counterclockwise(set, pos):
    move_servo(set.high.first, 180 - pos)
    move_servo(set.mid.first, pos)
    move_servo(set.low.first, 180 - pos)
#--------------------------------------------------
#SET LEVEL.<><><><><><><><><><><><><>
#--------------------------------------------------
def first_servos_smoth(set, other, direction, wight):
    if direction > 0:
        move_servo(set.high.first, set.high.first.pos - wight)
        move_servo(set.mid.first, set.mid.first.pos - wight)
        move_servo(set.low.first, set.low.first.pos - wight)
        print(set.high.first.pos)
        move_servo(other.high.first, other.high.first.pos - wight)
        move_servo(other.mid.first, other.mid.first.pos - wight)
        move_servo(other.low.first, other.low.first.pos - wight)
        print(other.high.first.pos)
    if direction < 0:
        move_servo(set.high.first, set.high.first.pos + wight)
        move_servo(set.mid.first, set.mid.first.pos + wight)
        move_servo(set.low.first, set.low.first.pos + wight)
        print(set.high.first.pos)
        move_servo(other.high.first, other.high.first.pos + wight)
        move_servo(other.mid.first, other.mid.first.pos + wight)
        move_servo(other.low.first, other.low.first.pos + wight)
        print(other.high.first.pos)

def three_servo_clockwise(set,other,direction, wight):
    if direction > 0:
        move_servo(set.high.first, set.high.first.pos - wight)
        move_servo(set.mid.first, set.mid.first.pos + wight)
        move_servo(set.low.first, set.low.first.pos - wight)
        print(set.high.first.pos)
        move_servo(other.high.first, other.high.first.pos + wight)
        move_servo(other.mid.first, other.mid.first.pos - wight)
        move_servo(other.low.first, other.low.first.pos + wight)
        print(other.high.first.pos)
    if direction < 0:
        move_servo(set.high.first, set.high.first.pos + wight)
        move_servo(set.mid.first, set.mid.first.pos - wight)
        move_servo(set.low.first, set.low.first.pos + wight)
        print(set.high.first.pos)
        move_servo(other.high.first, other.high.first.pos - wight)
        move_servo(other.mid.first, other.mid.first.pos + wight)
        move_servo(other.low.first, other.low.first.pos - wight)
        print(other.high.first.pos)
def move_set_up(set):
    move_three_servos(set.high.second, set.mid.second, set.low.second, 150)
    move_three_servos(set.high.third, set.mid.third, set.low.third, 180)

def move_set_down(set):
    for i in range(0, 90, 10):
        move_three_servos(set.high.second, set.mid.second, set.low.second, 150 - i)
        move_three_servos(set.high.third, set.mid.third, set.low.third, 130)

def move_set(set, pos):
    move_three_servos(set.high.second, set.mid.second, set.low.second, 180)
    move_three_servos(set.high.third, set.mid.third, set.low.third, 180)
    time.sleep(0.3)
    move_three_servos(set.high.first, set.mid.first, set.low.first, pos)
    time.sleep(0.1)
    move_three_servos(set.high.second, set.mid.second, set.low.second, 60)
    move_three_servos(set.high.third, set.mid.third, set.low.third, 90)



def move_set_limit(set, pos):
    move_three_servos(set.high.second, set.mid.second, set.low.second, 150)
    move_three_servos(set.high.third, set.mid.third, set.low.third, 170)
    time.sleep(0.3)
    move_three_servos(set.high.first, set.mid.first, set.low.first, pos)
    time.sleep(0.1)
    for i in range(0, 100, 10):
        if set.high.sensor.is_active() == False:
            move_two_servos(set.high.second, set.high.third, i)

        if set.mid.sensor.is_active() == False:
            move_two_servos(set.mid.second, set.mid.third, i)

        if set.low.sensor.is_active() == False:
            move_two_servos(set.low.second, set.low.third, i)
            
        if all_sensors_active() == True:
            body_up(set, 25)
            break
        time.sleep(0.06)

#--------------------------------------------------
#FINAL FUCNTION.<><><><><><><><><><><><><><><><><>
#--------------------------------------------------
class HEXAPOD:
    def __init__(self):
        pass

    def forward(self,lenght):
        set = left_set
        speed = 0.05
        wight = 5
        other = is_other_leg(set)
        move_set_limit(set, 120)
        time.sleep(0.2)
        for i in range(lenght * 10):
            first_servos_smoth(set, other,1, wight)
            
            if LHF.pos <= 70:
                move_set_limit(set, 120)
                time.sleep(0.2)

            if RHF.pos <= 70:
                move_set_limit(other, 120)
                time.sleep(0.2)
            #move_three_servos(other.high.first, other.mid.first, other.low.first, 120)
            print("done!!")
            time.sleep(speed)
        time.sleep(0.5)
        move_set_limit(set, 90)
        print("done!!")
#--------------------------------------------------
    def stand_up(self):
        move_set(left_set, 90)
        time.sleep(0.2)
        move_set(right_set, 90)
#--------------------------------------------------
    def turn_left(self,steps):
        for x in range(steps):
            for i in range(3):
                three_servo_clockwise(left_set, right_set, -1, 10)
                time.sleep(0.05)
            move_set(right_set, 90)
            time.sleep(0.5)
            move_set(left_set, 90)
            time.sleep(0.5)
#--------------------------------------------------
    def turn_right(self,steps):
        for x in range(steps):
            for i in range(3):
                three_servo_clockwise(left_set, right_set, 1, 10)
                time.sleep(0.05)
            move_set(left_set, 90)
            time.sleep(0.5)
            move_set(right_set, 90)
            time.sleep(0.5)
#--------------------------------------------------
    def defult_pos(self):
        for servo in [LHF, LHS, LHT, LMF, LMS, LMT, LLF, LLS, LLT, RHF, RHS, RHT, RMF, RMS, RMT, RLF, RLS, RLT]:
            move_servo(servo, 90)
            time.sleep(0.05)
#--------------------------------------------------
    def camera_left(self):
        for x in range(180):
            move_servo(camera, camera.pos + x)
            if camera.pos >= 180:
                break
            time.sleep(0.06)

    def camera_right(self):
        for x in range(180):
            move_servo(camera, camera.pos - x)
            if camera.pos <= 0:
                break
            time.sleep(0.06)

    def camera_center(self):
        move_servo(camera, 90)
    
    def dir_left(self):
        move_servo(camera, 180)
    
    def dir_right(self):
        move_servo(camera, 0)