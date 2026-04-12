import serial
import time
import platform
import legs
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
# --------------------------------------------------
#function to move a single servo to a target angle with optional speed control.
def move_servo(servo, target_angle, speed=100):
    if ser is None or not ser.is_open:
        print("⚠️ Serial port is not open!")
        return
    if servo.state == "right":
        target_angle = 180 - target_angle
    pulse = int(500 + (target_angle / 180.0) * 2000)
    
    try:
        command = f"#{servo.pin}P{pulse}S{speed}\r\n"
        servo.pos = pulse
        
        ser.write(command.encode())
    except Exception as e:
        print(f"❌ Error during transmission: {e}")

# --------------------------------------------------
#__helper functions__#
#--------------------------------------------------
#calculate the angle and the number of times to repeat the movement for angles greater than 20 degrees.
def angle_devider(angle):
    last_angle = angle % 20
    repeating_times = angle // 20
    return last_angle, repeating_times
#function to get the wanted set and the second set based on the input set.
def point_sets(set):
    if set == left_set:
        wanted_set = right_set
        second_set = left_set
    else:
        wanted_set = left_set
        second_set = right_set
    return wanted_set, second_set
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
#--------------------------------------------------
#use it for three servos at the same time.
def move_three_servos(servo1, servo2, servo3, pos):
    move_servo(servo1, pos)
    move_servo(servo2, pos)
    move_servo(servo3, pos)
#--------------------------------------------------
def move_three_servos_clockwise(set, pos):
    move_servo(set.high.first, pos)
    move_servo(set.mid.first, 180 - pos)
    move_servo(set.low.first, pos)
#------------------
def move_three_servos_counterclockwise(set, pos):
    move_servo(set.high.first, 180 - pos)
    move_servo(set.mid.first, pos)
    move_servo(set.low.first, 180 - pos)
#--------------------------------------------------
# just to set the legs up and move them to the position without putting them down.
def set_legs_up(set):
    move_three_servos(set.high.second, set.mid.second, set.low.second, 150)
    move_three_servos(set.high.third, set.mid.third, set.low.third, 180)
#---------------
#just to set the legs down after moving them up and forward or backward.
def set_legs_down(set):
    time.sleep(0.1)
    for i in range(0, 90, 5):
        move_three_servos(set.high.second, set.mid.second, set.low.second, 150 - i)
        move_three_servos(set.high.third, set.mid.third, set.low.third, 180 - i)
        time.sleep(0.05)
#--------------------------------------------------
#use it for a set of legs at the same time.
def move_set(set, pos):
    set_legs_up(set)
    time.sleep(0.5)
    set_legs_down(set)
move_three_servos_clockwise(left_set, 90)
#--------------------------------------------------
def push_forward(set):
    move_three_servos(set, 70)
#--------------------------------------------------
def push_backward(set):
    move_three_servos(set, 110)

#--------------------------------------------------
#function to get all servos to set on 90 degree.
def default_pos():
    for servo in [LHF, LHS, LHT, LMF, LMS, LMT, LLF, LLS, LLT, RHF, RHS, RHT, RMF, RMS, RMT, RLF, RLS, RLT]:
        move_servo(servo, 90)
#--------------------------------------------------
#started animations...

def started_turn_right(set, degree):
    wanted_set, second_set = point_sets(set)
    set_legs_up(wanted_set, degree)
    move_three_servos_clockwise(wanted_set, degree)
    move_three_servos_counterclockwise(second_set, degree)
    set_legs_down(wanted_set, degree)

def started_turn_left(set, degree):
    wanted_set, second_set = point_sets(set)

    set_legs_up(wanted_set, degree)
    move_three_servos_counterclockwise(wanted_set, degree)
    move_three_servos_clockwise(second_set, degree)
    set_legs_down(wanted_set, degree)

def started_for_ward(set, pos):
    wanted_set, second_set = point_sets(set)
    set_legs_up(wanted_set)
    push_forward(second_set)
    set_legs_down(wanted_set)

def started_back_ward(set, pos):
    wanted_set, second_set = point_sets(set)
    set_legs_up(wanted_set, pos)
    push_backward(second_set)
    set_legs_down(wanted_set)
#----------------------------------------------
#end face animations...
def end_turn_right(wanted_set, second_set, degree):
    pass
def end_turn_left(wanted_set, second_set, degree):
    pass
def end_for_ward(wanted_set, second_set, pos):
    pass
def end_back_ward(wanted_set, second_set, pos):
    pass
#--------------------------------------------------
#final function to move the robot in a direction with a specific degree or position.
set_legs_up(left_set)
set_legs_down(left_set)
set_legs_up(right_set)
set_legs_down(right_set)
default_pos()