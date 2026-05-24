import cv2
import subprocess
import numpy as np
import os
import time

# دالة التقاط الفريم وتحويله لرمادي
def get_camera_frame(temp_file="flow_temp.jpg"):
    cmd = [
        "rpicam-still", "-o", temp_file,
        "--width", "640", "--height", "480", 
        "--immediate", "-n"
    ]
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        frame = cv2.imread(temp_file)
        if frame is not None:
            return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    except Exception as e:
        print(f"خطأ في التقاط الفريم: {e}")
    return None

def main():
    print("🔄 جاري تشغيل نظام حساب المسافات بالتدفق البصري...")
    
    # الثوابت الفيزيائية والبرمجية الخاصة بالروبوت
    CAMERA_HEIGHT_CM = 5.0      # الارتفاع الحالي للروبوت عن الأرض
    FOCAL_LENGTH_PIXELS = 460.0 # البعد البؤري الثابت لكاميرا ov5647 بدقة 640x480
    
    # إعدادات خوارزمية التتبع
    feature_params = dict(maxCorners=100, qualityLevel=0.3, minDistance=7, blockSize=7)
    lk_params = dict(winSize=(15, 15), maxLevel=2,
                     criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))
    
    old_gray = get_camera_frame()
    if old_gray is None:
        print("❌ تعذر تشغيل الكاميرا.")
        return
        
    p0 = cv2.goodFeaturesToTrack(old_gray, mask=None, **feature_params)
    
    # متغير تراكمي لحساب المسافة الكلية التي قطعها الروبوت منذ تشغيل الكود
    total_distance_travelled_cm = 0.0
    
    print("🚀 بدأ الحساب! حرك الروبوت لمراقبة وقياس المسافة الحقيقية بالسنتيمتر...")
    
    try:
        while True:
            frame_gray = get_camera_frame()
            if frame_gray is None:
                continue
                
            if p0 is not None and len(p0) > 0:
                p1, st, err = cv2.calcOpticalFlowPyrLK(old_gray, frame_gray, p0, None, **lk_params)
                
                if p1 is not None:
                    good_new = p1[st == 1]
                    good_old = p0[st == 1]
                    
                    dx_total, dy_total = 0, 0
                    
                    for new, old in zip(good_new, good_old):
                        a, b = new.ravel()
                        c, d = old.ravel()
                        dx_total += (a - c)
                        dy_total += (b - d)
                    
                    if len(good_new) > 0:
                        # 1. متوسط حركة البكسلات في هذا الفريم
                        avg_dx = dx_total / len(good_new)
                        avg_dy = dy_total / len(good_new)
                        
                        # 2. حساب محصلة الحركة بالبكسل (وتر المثلث)
                        delta_pixel = np.sqrt(avg_dx**2 + avg_dy**2)
                        
                        # 3. القانون الرياضي: تحويل البكسل إلى سنتيمتر بناءً على الارتفاع 5 سم
                        distance_frame_cm = (delta_pixel * CAMERA_HEIGHT_CM) / FOCAL_LENGTH_PIXELS
                        
                        # تصفية الضوضاء الاهتزازية البسيطة للمحركات (Dead-zone filtering)
                        if distance_frame_cm > 0.05:
                            total_distance_travelled_cm += distance_frame_cm
                            print(f"📍 الإزاحة الحالية: {distance_frame_cm:.2f} سم | 🏁 المسافة الكلية المقطوعة: {total_distance_travelled_cm:.2f} سم")
                    
                    old_gray = frame_gray.copy()
                    p0 = good_new.reshape(-1, 1, 2)
            
            if p0 is None or len(p0) < 20:
                p0 = cv2.goodFeaturesToTrack(old_gray, mask=None, **feature_params)
                
    except KeyboardInterrupt:
        print(f"\n🛑 تم إيقاف التتبع. المسافة النهائية الإجمالية: {total_distance_travelled_cm:.2f} سم")
    finally:
        if os.path.exists("flow_temp.jpg"):
            os.remove("flow_temp.jpg")

if __name__ == "__main__":
    main()