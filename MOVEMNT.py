import serial
import time
import platform
import legs

# 1. فتح المنفذ مرة واحدة فقط وإعداده بسرعة عالية (Baudrate)
def get_servo_port():
    current_os = platform.system()
    return "COM5" if current_os == "Windows" else "/dev/ttyUSB0"

# يفضل رفع الـ Baudrate إلى 115200 إذا كانت اللوحة تدعم ذلك
ser = serial.Serial(get_servo_port(), 115200, timeout=0.01) 

# 2. وظيفة إرسال "مجموعة" محركات في أمر واحد (Group Command)
# هذا هو السر الحقيقي للسرعة في لوحات تحكم المحركات
def move_servos_group(servo_list, angles, speed=100):
    """
    servo_list: قائمة بكائنات المحركات
    angles: قائمة بالزوايا المقابلة
    """
    command = ""
    for servo, angle in zip(servo_list, angles):
        pulse = int(500 + (angle / 180.0) * 2000)
        command += f"#{servo.pin}P{pulse}"
        servo.pos = pulse
    
    command += f"S{speed}\r\n"
    try:
        ser.write(command.encode())
    except Exception as e:
        print(f"❌ Serial Error: {e}")

# -------------------------------------------------
# تحسين وظائف المجموعات لتكون أسرع (ترسل الأوامر معاً)
# -------------------------------------------------

def move_set_xcor_fast(leg_set, degree, speed=200):
    # إرسال أوامر المحركات الثلاثة في "نبضة" واحدة عبر السلك
    servos = [leg_set.high.first, leg_set.mid.first, leg_set.low.first]
    angles = [degree, degree, degree]
    move_servos_group(servos, angles, speed)

def set_up_fast(leg_set, speed=200):
    servos = [
        leg_set.high.second, leg_set.high.third,
        leg_set.mid.second, leg_set.mid.third,
        leg_set.low.second, leg_set.low.third
    ]
    # رفع الأرجل (الزوايا كما في كودك الأصلي)
    angles = [160, 20, 160, 20, 160, 20]
    move_servos_group(servos, angles, speed)

def set_down_fast(leg_set, degree, speed=150):
    # تحريك المفاصل الأساسية للأرجل الثلاثة معاً
    servos = [leg_set.high.first, leg_set.mid.first, leg_set.low.first]
    angles = [degree, degree, degree]
    move_servos_group(servos, angles, speed)
    # ملاحظة: كود الحساسات يحتاج لتعديل ليعمل بالتوازي (Multi-threading)
    # لكن حالياً، الإرسال الجماعي سيسرع العملية جداً.

# -------------------------------------------------
# تعديل وظيفة الحركة للأمام لتكون انسيابية
# -------------------------------------------------

def forward_fast():
    # ارفع مجموعة وحرك الأخرى (كل مجموعة كأمر واحد)
    set_up_fast(right_set)
    move_set_xcor_fast(left_set, 70) 
    time.sleep(0.1) # انتظار بسيط جداً
    
    set_up_fast(left_set)
    move_set_xcor_fast(right_set, 90)
    time.sleep(0.1)

# -------------------------------------------------
# تعريف المحركات والأرجل (كما في كودك الأصلي)
# -------------------------------------------------
# ... (ضع تعريفات LHF, LHS... الخ هنا)

if __name__ == "__main__":
    # تجربة حركة سريعة
    print("🚀 Starting Fast Movement...")
    forward_fast()