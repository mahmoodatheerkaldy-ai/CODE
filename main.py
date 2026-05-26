import sys
import tty
import termios
import time
import select
import STRINGTH as st
from camertest import capture_image

# Initialize the Hexapod motion object
try:
    s = st.HEXAPOD()
    HAS_HARDWARE = True
except Exception as e:
    print(f"⚠️ Hardware Initialization Error: {e}")
    HAS_HARDWARE = False

def update_screen(log_message="", charging_status=""):
    """تمسح الشاشة بالكامل وتعيد طباعة اللوحة الثابتة مع الحالة الحالية للروبوت لمنع الاختفاء"""
    # مسح الشاشة بالكامل وإرجاع المؤشر للأعلى
    sys.stdout.write("\033[H\033[J") 
    
    print("====================================================")
    print("      [SPECTER FIXED DASHBOARD CONTROLLER]          ")
    print("====================================================")
    print(" 🕹️  MOVEMENT CONTROLS:")
    print("    W : Forward (+10 units)  |  S : Backward (+10 units)")
    print("    A : Turn Left (+30 deg)  |  D : Turn Right (+30 deg)")
    print("    SPACEBAR : Execute accumulated movement")
    print("----------------------------------------------------")
    print(" 📸  CAMERA CONTROLS:")
    print("    C : Center Camera (90°) & Capture Image")
    print("    L : Turn Camera 90° LEFT  (To 0° Position)")
    print("    R : Turn Camera 90° RIGHT (To 180° Position)")
    print("----------------------------------------------------")
    print(" ⚙️  SYSTEM CONTROLS:")
    print("    X : Default/Sleep Position")
    print("    Q : Quit Program")
    print("====================================================")
    print(" 🔋 STATUS / CHARGING BUFFER:")
    if charging_status:
        print(f"    {charging_status}")
    else:
        print("    Idle... Awaiting movement commands.")
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
    update_screen(log_message="System Online. Ready for Specter inputs.")
    
    accumulated_key = None
    click_count = 0
    current_log = "System Online. Ready for Specter inputs."
    
    try:
        while True:
            key = getch_timeout(timeout=0.05)
            
            if key is not None:
                if key == 'q':
                    sys.stdout.write("\033[H\033[J")
                    print("🛑 Exiting program. Goodbye Mahmood!")
                    break
                
                # 1. Center & Capture
                elif key == 'c':
                    update_screen(log_message="📸 [CAMERA] Centering camera (90°) and taking picture...")
                    if HAS_HARDWARE:
                        if hasattr(s, 'set_camera_angle'): s.set_camera_angle(90)
                        time.sleep(0.3)
                        try:
                            s.camera_center()
                            time.sleep(1)
                            capture_image()
                            current_log = "✅ [CAMERA] Picture captured successfully at 90°!"
                        except Exception as e:
                            s.camera_center()
                            time.sleep(1)
                            capture_image()
                            current_log = "✅ [CAMERA] Picture forced captured!"
                    else:
                        current_log = "📸 [CAMERA] Simulation Mode - Image Taken."
                    update_screen(log_message=current_log)
                
                # 2. Camera 90° LEFT
                elif key == 'l':
                    update_screen(log_message="🎥 [CAMERA] Turning 90° LEFT (Target: 0°)...")
                    if HAS_HARDWARE:
                        if hasattr(s, 'set_camera_angle'): 
                            current_log = "Moving hardware to 0 degrees!"
                        else:
                            s.dir_left()
                            time.sleep(1)
                            capture_image()
                            current_log = "🎥 Left Turn & Capture Complete."
                    else:
                        current_log = "🎥 [CAMERA] Simulation Mode - Turned Left."
                    update_screen(log_message=current_log)
                
                # 3. Camera 90° RIGHT
                elif key == 'r':
                    update_screen(log_message="🎥 [CAMERA] Turning 90° RIGHT (Target: 180°)...")
                    if HAS_HARDWARE:
                        if hasattr(s, 'set_camera_angle'): 
                            current_log = "Moving hardware to 180 degrees!"
                        else:
                            s.dir_right()
                            time.sleep(1)
                            capture_image()
                            current_log = "🎥 Right Turn & Capture Complete."
                    else:
                        current_log = "🎥 [CAMERA] Simulation Mode - Turned Right."
                    update_screen(log_message=current_log)

                # 4. Accumulate Movement
                elif key in ['w', 's', 'a', 'd']:
                    if key != accumulated_key:
                        accumulated_key = key
                        click_count = 1
                    else:
                        click_count += 1
                    
                    if accumulated_key in ['w', 's']:
                        current_value = click_count * 10
                        unit_str = "units"
                    else:
                        current_value = click_count * 30
                        unit_str = "degrees"
                        
                    status_str = f"Key: [{accumulated_key.upper()}] | Clicks: {click_count} -> Total: {current_value} {unit_str} | (SPACE to execute)"
                    update_screen(log_message=current_log, charging_status=status_str)
                
                # 5. Spacebar - Execute Movement
                elif key == ' ':
                    if accumulated_key is None or click_count == 0:
                        update_screen(log_message="⚠️ [SYSTEM] Buffer empty! Charge a direction first.")
                        continue
                    
                    executed_key = accumulated_key
                    total_clicks = click_count
                    
                    accumulated_key = None
                    click_count = 0
                    
                    if executed_key == 'w':
                        units = total_clicks * 10
                        update_screen(log_message=f"💥 [EXECUTE] Walking FORWARD by {units} units...")
                        if HAS_HARDWARE: s.forward(units)
                        current_log = f"✅ Move done: FORWARD {units} units"
                                
                    elif executed_key == 's':
                        units = total_clicks * 10
                        update_screen(log_message=f"💥 [EXECUTE] Walking BACKWARD by {units} units...")
                        if HAS_HARDWARE: s.backward(units)
                        current_log = f"✅ Move done: BACKWARD {units} units"
                        
                    elif executed_key == 'a':
                        degrees = total_clicks * 30
                        update_screen(log_message=f"💥 [EXECUTE] Turning LEFT by {degrees} degrees...")
                        if HAS_HARDWARE: s.turn_left(degrees)
                        current_log = f"✅ Turn done: LEFT {degrees} degrees"
                        
                    elif executed_key == 'd':
                        degrees = total_clicks * 30
                        update_screen(log_message=f"💥 [EXECUTE] Turning RIGHT by {degrees} degrees...")
                        if HAS_HARDWARE: s.turn_right(degrees)
                        current_log = f"✅ Turn done: RIGHT {degrees} degrees"
                        
                    update_screen(log_message=current_log)

                # 6. Sleep Position
                elif key == 'x':
                    accumulated_key = None
                    click_count = 0
                    update_screen(log_message="💤 [SLEEP] Moving to default position...")
                    if HAS_HARDWARE: s.default_pos()
                    current_log = "💤 Robot is now in SLEEP mode."
                    update_screen(log_message=current_log)

    except KeyboardInterrupt:
        sys.stdout.write("\033[H\033[J")
        print("🛑 Program interrupted.")

if __name__ == "__main__":
    main()