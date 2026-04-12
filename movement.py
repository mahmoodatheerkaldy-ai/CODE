import serial
import time
import platform
import legs
#------------------------------------------------
#define servos..
LHF = legs.servo(1, 90)
LHS = legs.servo(2, 90)
LHT = legs.servo(3, 90)
LMF = legs.servo(4, 90)
LMS = legs.servo(5, 90)
LMT = legs.servo(6, 90)
LLF = legs.servo(7, 90)
LLS = legs.servo(8, 90)
LLT = legs.servo(9, 90)
RHF = legs.servo(32, 90)
RHS = legs.servo(31, 90)
RHT = legs.servo(30, 90)
RMF = legs.servo(29, 90)
RMS = legs.servo(28, 90)
RMT = legs.servo(27, 90)
RLF = legs.servo(26, 90)
RLS = legs.servo(25, 90)
RLT = legs.servo(24, 90)
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
right_high = legs.leg(LHF, LHS, LHT, LH)
right_mid = legs.leg(LMF, LMS, LMT, LM)
right_low = legs.leg(LLF, LLS, LLT, LL)
left_high = legs.leg(RHF, RHS, RHT, RH)
left_mid = legs.leg(RMF, RMS, RMT, RM)
left_low = legs.leg(RLF, RLS, RLT, RL)
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
    # نفتح الاتصال هنا ونتركه مفتوحاً
    ser = serial.Serial(port, 9600, timeout=1)
    print(f"✅ Serial Port {port} Opened Successfully.")
except Exception as e:
    print(f"❌ Failed to open port: {e}")
    ser = None
# --------------------------------------------------
#define 
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
def move_leg(leg, pos):
    move_servo(leg.first, pos)
    move_servo(leg.second, 150)
    move_servo(leg.third, 180)
    time.sleep(0.1)
    for i in range(0, 90, 5):
        move_servo(leg.second, 150 - i)
        move_servo(leg.third, 180 - i)
        time.sleep(0.1)
move_leg(right_high, 120)
def test():
    move_servo(LHF, 90)
    move_servo(LHS, 90)
    move_servo(LHT, 90)
test()
move_leg(right_high, 120)

#50 - 130
#60 - 150
#90 - 180
move_servo(RHF, 120)
