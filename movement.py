import serial
import time
import platform
import legs
import threading as devil
#------------------------------------------------
#define servos..
LHF = legs.left_servo(1, 90)
LHS = legs.left_servo(2, 90)
LHT = legs.left_servo(3, 90)
LMF = legs.left_servo(4, 90)
LMS = legs.left_servo(5, 90)
LMT = legs.left_servo(6, 90)
LLF = legs.left_servo(7, 90)
LLS = legs.left_servo(8, 90)
LLT = legs.left_servo(9, 90)
RHF = legs.right_servo(32, 90)
RHS = legs.right_servo(31, 90)
RHT = legs.right_servo(30, 90)
RMF = legs.right_servo(29, 90)
RMS = legs.right_servo(28, 90)
RMT = legs.right_servo(27, 90)
RLF = legs.right_servo(26, 90)
RLS = legs.right_servo(25, 90)
RLT = legs.right_servo(24, 90)
#-------------------------------------------------
#define sensors...
LH = legs.limit_switch(1)
LM = legs.limit_switch(2)
LL = legs.limit_switch(3)
RH = legs.limit_switch(4)
RM = legs.limit_switch(5)
RL = legs.limit_switch(6)
#-------------------------------------------------
#define legs...
left_high = legs.leg(LHF, LHS, LHT, LH)
left_mid = legs.leg(LMF, LMS, LMT, LM)
left_low = legs.leg(LLF, LLS, LLT, LL)
right_high = legs.leg(RHF, RHS, RHT, RH)
right_mid = legs.leg(RMF, RMS, RMT, RM)
right_low = legs.leg(RLF, RLS, RLT, RL)

#-------------------------------------------------
#define sets of legs...
left_set = legs.set_of_legs(left_high, right_mid, left_low)
right_set = legs.set_of_legs(right_high, left_mid, right_low)
#--------------------------------------------------
#define port...
def get_servo_port():
    current_os = platform.system()
    if current_os == "Windows":
        return "COM5"
    return "/dev/ttyUSB0"

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
    
#--------------------------------------------------
def default_pos():
    for servo in [LHF, LHS, LHT, LMF, LMS, LMT, LLF, LLS, LLT, RHF, RHS, RHT, RMF, RMS, RMT, RLF, RLS, RLT]:
        move_servo(servo, 90)
        time.sleep(0.05)
#--------------------------------------------------
#LEG LEVEL.<><><><><><><><><><><><><>
#--------------------------------------------------
#use it for one leg at a time.
def move_leg(leg, pos):
    move_servo(leg.second, 150)
    move_servo(leg.third, 180)
    time.sleep(0.3)
    move_servo(leg.first, pos)
    time.sleep(0.1)
    for i in range(0, 90, 5):
        move_servo(leg.second, 150 - i)
        move_servo(leg.third, 180 - i)
        time.sleep(0.05)

def move_three_servos(servo1, servo2, servo3, pos):
    move_servo(servo1, pos)
    move_servo(servo2, pos)
    move_servo(servo3, pos)


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

#--------------------------------------------------
#FINAL FUCNTION.<><><><><><><><><><><><><><><><><>
#--------------------------------------------------
def forward(set,lenght):
    speed = 0.05
    wight = 5
    other = is_other_leg(set)
    move_set(set, 120)
    for i in range(lenght):
        first_servos_smoth(set, other,1, wight)
        
        if LHF.pos <= 70:
            t = devil.Thread(target=move_set, args=(set, 120,))
            t.start()
            time.sleep(0.5)

        if RHF.pos <= 70:
            t2 = devil.Thread(target=move_set, args=(other, 120,))
            t2.start()
            time.sleep(0.5)
            move_three_servos(other.high.first, other.mid.first, other.low.first, 120)
        print("done!!")
        time.sleep(speed)
    time.sleep(0.5)
    move_set(set, 90)
#--------------------------------------------------
def stand_up():
    move_set(left_set, 90)
    time.sleep(0.2)
    move_set(right_set, 90)
#--------------------------------------------------
def turn_left():
    for x in range(3):
        for i in range(3):
            three_servo_clockwise(left_set, right_set, -1, 10)
            time.sleep(0.05)
        move_set(right_set, 90)
        time.sleep(0.5)
        move_set(left_set, 90)
        time.sleep(0.5)
def turn_right():
    for x in range(3):
        for i in range(3):
            three_servo_clockwise(left_set, right_set, 1, 10)
            time.sleep(0.05)
        move_set(left_set, 90)
        time.sleep(0.5)
        move_set(right_set, 90)
        time.sleep(0.5)

turn_left()
turn_right()
default_pos()
stand_up()
three_servo_clockwise(left_set, right_set, 1, 10)