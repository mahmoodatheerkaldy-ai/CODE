import sys
import tty
import termios
import time
import select
import STRINGTH as st
from camertest import capture_image
from moisture import get_moisture

# Initialize the Hexapod motion object
try:
    s = st.HEXAPOD()
    HAS_HARDWARE = True
except Exception as e:
    print(f"⚠️ Hardware Initialization Error: {e}")
    HAS_HARDWARE = False

def update_screen(log_message="", charging_status=""):
    """مسح الشاشة وإعادة طباعة اللوحة الثابتة"""
    sys.stdout.write("\033[H\033[J") 
    
    print("====================================================")
    print("      [SPECTER FIXED DASHBOARD CONTROLLER]          ")
    print("====================================================")
    print(" 🕹️  MOV: W/S, A/D | SPACE: Execute")
    print(" 📸  CAM: C (Center) | L: Left | R: Right")
    print(" 🧪  SENSOR: M (Moisture) | U: Ready | O: Off")
    print(" ↕️  BODY: F (Down 5) | G (Up 5)")
    print(" ⚙️  SYS: X (Sleep) | P (Stand Up) | Q (Quit)")
    print("====================================================")
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

def main():
    flush_input_buffer()
    current_log = "System Online. Ready for Specter inputs."
    update_screen(log_message=current_log)
    
    accumulated_key = None
    click_count = 0
    
    try:
        while True:
            key = getch_timeout(timeout=0.05)
            
            if key is not None:
                if key == 'q':
                    sys.stdout.write("\033[H\033[J")
                    print("🛑 Exiting program. Goodbye Mahmood!")
                    break
                
                # أوامر النظام
                elif key == 'p':
                    if HAS_HARDWARE: s.stand_up()
                    current_log = "🧍 [POSTURE] Robot is standing up."
                
                elif key == 'x':
                    if HAS_HARDWARE: s.default_pos()
                    current_log = "💤 Robot is in SLEEP mode."
                
                # أوامر الحساس
                elif key == 'm':
                    val = get_moisture()
                    current_log = f"💧 Moisture: {val:.1f}%"
                
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
                
                # الكاميرا - التحديثات الجديدة
                elif key == 'c':
                    if HAS_HARDWARE:
                        s.camera_center()
                        time.sleep(0.5)
                        capture_image()
                    current_log = "✅ [CAMERA] Centered & Captured!"
                
                elif key == 'l':
                    if HAS_HARDWARE:
                        s.dir_left()
                        time.sleep(0.5)
                        capture_image()
                    current_log = "🎥 [CAMERA] Turned LEFT & Captured!"
                
                elif key == 'r':
                    if HAS_HARDWARE:
                        s.dir_right()
                        time.sleep(0.5)
                        capture_image()
                    current_log = "🎥 [CAMERA] Turned RIGHT & Captured!"
                
                # الحركة
                elif key in ['w', 's', 'a', 'd']:
                    accumulated_key = key
                    click_count += 1
                    status_str = f"Buffering: [{key.upper()}] x{click_count} (Total: {click_count*10} units)"
                    update_screen(log_message=current_log, charging_status=status_str)
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
                
                update_screen(log_message=current_log)

    except KeyboardInterrupt:
        sys.stdout.write("\033[H\033[J")
        print("🛑 Program interrupted.")

if __name__ == "__main__":
    main()