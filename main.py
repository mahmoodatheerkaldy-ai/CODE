import sys
import tty
import termios
import time
import select
import STRINGTH as st
from camertest import capture_image
from moisture import get_moisture
from analyzer import plot_moisture_3d  # استيراد ملف التحليل ثلاثي الأبعاد

# Initialize the Hexapod motion object2
try:
    s = st.HEXAPOD()
    HAS_HARDWARE = True
except Exception as e:
    print(f"⚠️ Hardware Initialization Error: {e}")
    HAS_HARDWARE = False

# متغيرات الخريطة العالمية
moisture_map = []
ROWS = 0
STEPS = 0
current_row = 0
current_step = 0

def update_screen(log_message="", charging_status="", min_moisture=20.0):
    """مسح الشاشة وإعادة طباعة اللوحة الثابتة"""
    sys.stdout.write("\033[H\033[J") 
    
    # عرض الإحداثيات بطريقة مفهومة للمخدم (تبدأ من 1)
    display_row = current_row + 1 if current_row < ROWS else ROWS
    display_step = current_step + 1 if current_step < STEPS else STEPS
    
    print("====================================================")
    print("      [SPECTER FIXED DASHBOARD CONTROLLER]          ")
    print("====================================================")
    print(" 🕹️  MOV: W/S, A/D | SPACE: Execute")
    print(" 📸  CAM: C (Center) | L: Left | R: Right")
    print(" 🧪  SENSOR: M (Moisture) | U: Ready | O: Off")
    print(" ↕️  BODY: F (Down 5) | G (Up 5)")
    print(" ⚙️  SYS: X (Sleep) | P (Stand Up) | Q (Quit)")
    print("====================================================")
    print(f" 📐 Threshold: {min_moisture}% | Grid Size: {ROWS}x{STEPS}")
    print(f" 📍 Current Target Position: [Row {display_row}, Step {display_step}]")
    print("----------------------------------------------------")
    print(" 🔋 STATUS / CHARGING BUFFER:")
    if charging_status:
        print(f"    {charging_status}")
    else:
        print("    Idle... Awaiting commands.")
    print("----------------------------------------------------")
    print(" 📢  LAST ACTION LOG:")
    print(f"    {log_message}")
    print("====================================================")
    sys.stdout.flush()

def flush_input_buffer():
    try:
        termios.tcflush(sys.stdin, termios.TCIFLUSH)
    except Exception:
        pass

def getch_timeout(timeout=0.05):
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        r, _, _ = select.select([sys.stdin], [], [], timeout)
        if r:
            return sys.stdin.read(1).lower()
        return None
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

def print_final_map():
    """طباعة المصفوفة بشكل منظم ومفهوم للمستخدم"""
    print("\n" + "="*50)
    print("📊 FINAL SOIL MOISTURE MAP (2D LIST):")
    print("="*50)
    for i, row in enumerate(moisture_map):
        formatted_row = [f"{val:.1f}%" for val in row]
        print(f"Row {i+1}: {formatted_row}")
    print("="*50)

def main():
    global moisture_map, ROWS, STEPS, current_row, current_step
    
    # 1. طلب الأبعاد والحد الأدنى من المستخدم قبل الدخول في تفعيل التيرمنال
    try:
        print("--- GRID CONFIGURATION ---")
        ROWS = int(input("Enter number of Rows (Lines): "))
        STEPS = int(input("Enter number of Steps per row: "))
        MIN_MOISTURE = float(input("Enter minimum acceptable moisture % (e.g. 20): "))
        
        # إنشاء مصفوفة مسبقة الأبعاد ممتلئة بأصفار
        moisture_map = [[0.0 for _ in range(STEPS)] for _ in range(ROWS)]
        
    except ValueError:
        print("⚠️ Invalid inputs! Setting default grid to 2x4 and threshold 20.0%")
        ROWS, STEPS = 2, 4
        MIN_MOISTURE = 20.0
        moisture_map = [[0.0 for _ in range(STEPS)] for _ in range(ROWS)]
        time.sleep(2)

    flush_input_buffer()
    current_log = f"System Online. Grid {ROWS}x{STEPS} ready. Threshold: {MIN_MOISTURE}%"
    update_screen(log_message=current_log, min_moisture=MIN_MOISTURE)
    
    accumulated_key = None
    click_count = 0
    is_map_full = False
    
    try:
        while True:
            # إذا امتلأت المصفوفة بالكامل، اخرج من الحلقة تلقائياً واعرض الرسم والنتائج
            if is_map_full:
                sys.stdout.write("\033[H\033[J")
                print("🎉 Excellent! All coordinates have been mapped successfully.")
                print_final_map()
                plot_moisture_3d(moisture_map, MIN_MOISTURE)  # استدعاء المخطط 3D تلقائياً عند الاكتمال
                break

            key = getch_timeout(timeout=0.05)
            
            if key is not None:
                if key == 'q':
                    sys.stdout.write("\033[H\033[J")
                    print("🛑 Exiting program. Goodbye Mahmood!")
                    print_final_map()
                    # فتح الرسم بما تم جمعه قبل الخروج الاختياري
                    if any(any(val > 4.0 for val in r) for r in moisture_map):
                        plot_moisture_3d(moisture_map, MIN_MOISTURE)
                    break
                
                # أوامر النظام
                elif key == 'p':
                    if HAS_HARDWARE: s.stand_up()
                    current_log = "🧍 [POSTURE] Robot is standing up."
                
                elif key == 'x':
                    if HAS_HARDWARE: s.default_pos()
                    current_log = "💤 Robot is in SLEEP mode."
                
                # أمر الحساس الذكي مع الإدخال والتحريك التلقائي
                elif key == 'm':
                    val = get_moisture()
                    
                    if val > 4.0:
                        # تخزين القراءة في المكان الحالي
                        moisture_map[current_row][current_step] = val
                        
                        # فحص التنبيه للرطوبة المنخفضة
                        if val < MIN_MOISTURE:
                            log_status = f"⚠️ [ALERT] Low Moisture! {val:.1f}%"
                        else:
                            log_status = f"💧 Saved: {val:.1f}%"
                            
                        current_log = f"{log_status} at [Row {current_row+1}, Step {current_step+1}]"
                        
                        # الانتقال التلقائي للخانة التالية
                        current_step += 1
                        if current_step >= STEPS:      # إذا انتهى السطر الحالي
                            current_step = 0           # صفر الخطوات
                            current_row += 1           # انتقل للسطر التالي تلقائياً
                            
                        if current_row >= ROWS:        # إذا انتهت كل الأسطر
                            is_map_full = True         # تفعيل علم الامتلاء
                    else:
                        current_log = f"⚠️ [IGNORED] Reading {val:.1f}% <= 4% (Sensor in air)."
                
                elif key == 'u':
                    if HAS_HARDWARE: s.get_mos_ready()
                    current_log = "✅ [SYSTEM] Moisture sensor READY."
                
                elif key == 'o':
                    if HAS_HARDWARE: s.get_mos_off()
                    current_log = "❌ [SYSTEM] Moisture sensor OFF."
                
                # أوامر الجسم
                elif key == 'f':
                    if HAS_HARDWARE: s.all_body_down(5)
                    current_log = "⬇️ [BODY] Lowered by 5."
                
                elif key == 'g':
                    if HAS_HARDWARE: s.all_body_up(5)
                    current_log = "⬆️ [BODY] Raised by 5."
                
                # الكاميرا
# الكاميرا في ملف main.py
                elif key == 'c':
                    if HAS_HARDWARE:
                        s.camera_center()
                        time.sleep(0.5)
                        # استقبال نتيجة الذكاء الاصطناعي وعرضها في اللوج
                        current_log = capture_image() 
                
                elif key == 'l':
                    if HAS_HARDWARE:
                        s.dir_left()
                        time.sleep(0.5)
                        current_log = capture_image()
                
                elif key == 'r':
                    if HAS_HARDWARE:
                        s.dir_right()
                        time.sleep(0.5)
                        current_log = capture_image()
                # الحركة
                elif key in ['w', 's', 'a', 'd']:
                    accumulated_key = key
                    click_count += 1
                    status_str = f"Buffering: [{key.upper()}] x{click_count} (Total: {click_count*10} units)"
                    update_screen(log_message=current_log, charging_status=status_str, min_moisture=MIN_MOISTURE)
                    continue
                
                elif key == ' ':
                    if accumulated_key:
                        if HAS_HARDWARE:
                            if accumulated_key == 'w': s.forward(click_count * 10)
                            elif accumulated_key == 's': s.backward(click_count * 10)
                            elif accumulated_key == 'a': s.turn_left(click_count * 30)
                            elif accumulated_key == 'd': s.turn_right(click_count * 30)
                        current_log = f"✅ Executed {accumulated_key.upper()} x{click_count}"
                        accumulated_key = None
                        click_count = 0
                
                update_screen(log_message=current_log, min_moisture=MIN_MOISTURE)

    except KeyboardInterrupt:
        sys.stdout.write("\033[H\033[J")
        print("🛑 Program interrupted by user.")
        print_final_map()
        # عرض الرسم البياني الجزئي في حال الإغلاق بـ Ctrl+C
        if any(any(val > 4.0 for val in r) for r in moisture_map):
            print("📊 Showing 3D diagram for collected data before interruption...")
            plot_moisture_3d(moisture_map, MIN_MOISTURE)

if __name__ == "__main__":
    main()