import cv2
import subprocess
import numpy as np
import os

def main():
    print("جاري استدعاء حساس الكاميرا عبر بايبلاين النظام (rpicam-still)...")
    
    # اسم الملف المؤقت لحفظ الصورة من النظام
    temp_filename = "temp_capture.jpg"
    final_filename = "plant_test.jpg"
    
    try:
        # أمر النظام لالتقاط صورة فورية بدون عرض نافذة (v4l2/libcamera native)
        # ضبط الدقة إلى 1296x972 وهي دقة ممتازة جداً لمعالجة الصور و YOLO
        cmd = [
            "rpicam-still",
            "-o", temp_filename,
            "--width", "1296",
            "--height", "972",
            "--immediate",       # التقاط فوري بدون انتظار 5 ثوانٍ للاستعراض
            "-n"                 # عدم فتح نافذة عرض (No preview) لتجنب أخطاء الـ SSH
        ]
        
        # تنفيذ الأمر برمجياً
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        if os.path.exists(temp_filename):
            print("✅ نجح النظام في التقاط الصورة. جاري تمريرها إلى OpenCV...")
            
            # قراءة الصورة عبر OpenCV لتصبح على شكل مصفوفة (Numpy Array) جاهزة للـ AI
            frame = cv2.imread(temp_filename)
            
            if frame is not None:
                # حفظ الصورة النهائية في مجلد المشروع للتأكد
                cv2.imwrite(final_filename, frame)
                print(f"🎉 مبروك! الصورة جاهزة الآن ومحفوظة باسم: {final_filename}")
                print(f"أبعاد المصفوفة الحالية: {frame.shape}") # للتأكد من الـ Matrix
                
                # هنا مستقبلاً يمكنك تمرير المصفوفة مباشرة إلى موديل الـ YOLO:
                # results = model(frame)
            else:
                print("❌ فشل OpenCV في قراءة ملف الصورة الناتج.")
                
            # تنظيف النظام وحذف الملف المؤقت
            os.remove(temp_filename)
        else:
            print("❌ لم يتم العثور على الملف المؤقت بعد التقاطه.")
            
    except subprocess.CalledProcessError as e:
        print(f"❌ فشل بايبلاين النظام في التقاط الصورة: {e}")
    except Exception as e:
        print(f"❌ حدث خطأ غير متوقع: {e}")

if __name__ == "__main__":
    main()