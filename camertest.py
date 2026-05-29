import cv2
import subprocess
import numpy as np
import os
from ultralytics import YOLO  # استيراد مكتبة الـ AI

# تحميل موديل الـ Detection من نفس المجلد
MODEL_PATH = "best.pt"
model = None

try:
    if os.path.exists(MODEL_PATH):
        # تحميل الموديل وتوجيهه للـ CPU مباشرة وإلغاء الـ mmap لمنع الـ Bus error
        model = YOLO(MODEL_PATH)
        model.to('cpu') 
        print("🧠 [AI] YOLO Detection model loaded successfully on CPU!")
    else:
        print(f"⚠️ [AI] Warning: '{MODEL_PATH}' not found in this folder. AI classification will be skipped.")
except Exception as e:
    model = None
    print(f"⚠️ [AI] Failed to load model: {e}")


def capture_image():
    print("جاري استدعاء حساس الكاميرا عبر بايبلاين النظام (rpicam-still)...")
    
    # اسم الملف المؤقت لحفظ الصورة من النظام
    temp_filename = "temp_capture.jpg"
    final_filename = "plant_test.jpg"
    
    # المتغير الذي سنعيده للبرنامج الرئيسي ليعرضه في اللوحة (الـ LOG)
    ai_log_result = "Camera Centered & Captured!"
    
    try:
        # أمر النظام لالتقاط صورة فورية بدون عرض نافذة
        cmd = [
            "rpicam-still",
            "-o", temp_filename,
            "--width", "1296",
            "--height", "972",
            "--immediate",       # التقاط فوري بدون انتظار
            "-n"                 # عدم فتح نافذة عرض (لتجنب أخطاء الـ SSH)
        ]
        
        # تنفيذ الأمر برمجياً
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        if os.path.exists(temp_filename):
            print("✅ نجح النظام في التقاط الصورة. جاري تمريرها إلى OpenCV...")
            
            # قراءة الصورة عبر OpenCV لتصبح على شكل مصفوفة جاهزة للـ AI
            frame = cv2.imread(temp_filename)
            
            if frame is not None:
                # حفظ الصورة النهائية الأصلية في مجلد المشروع للتأكد
                cv2.imwrite(final_filename, frame)
                print(f"🎉 مبروك! الصورة جاهزة الآن ومحفوظة باسم: {final_filename}")
                
                # --- تشغيل فحص الذكاء الاصطناعي (AI Object Detection) ---
                if model is not None:
                    print("🧠 [AI] Analyzing image with YOLO (Detection Mode)...")
                    
                    # 1. تصحيح نظام الألوان من BGR الخاص بـ OpenCV إلى RGB الذي يفضله YOLO
                    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    
                    # 2. تشغيل التنبؤ مع ضبط حد الثقة (conf) وأبعاد الصورة المناسبة للشبكة العصبية
                    results = model.predict(source=rgb_frame, conf=0.20, imgsz=640, verbose=False)
                    
                    # 3. التحقق من وجود صناديق مكتشفة (Boxes) في مخرجات الموديل
                    if results and len(results) > 0 and results[0].boxes is not None and len(results[0].boxes) > 0:
                        
                        # الحصول على الصندوق الأول (صاحب أعلى نسبة ثقة تلقائياً)
                        best_box = results[0].boxes[0]
                        
                        # استخراج الرقم التعريفي للكلاس، اسم الكلاس، ونسبة الثقة
                        class_idx = int(best_box.cls[0].item())
                        class_name = results[0].names[class_idx]
                        confidence = best_box.conf[0].item() * 100
                        
                        # تجهيز نص النتيجة لعرضه في لوحة التحكم (LAST ACTION LOG)
                        ai_log_result = f"📸 [AI RESULT]: {class_name} ({confidence:.1f}%)"
                        print(f"✅ {ai_log_result}")
                        
                        # [ميزة إضافية]: رسم المربع المحيط بالهدف على الصورة وحفظها لتظهر بالواجهة الرسومية مرسومة
                        res_plotted = results[0].plot()
                        cv2.imwrite(final_filename, cv2.cvtColor(res_plotted, cv2.COLOR_RGB2BGR))
                    else:
                        ai_log_result = "📸 Captured! [AI] No objects detected above threshold."
                        print("⚠️ لم يتم كشف أي كائنات أو مربعات في الصورة.")
                else:
                    ai_log_result = "📸 Captured! (AI model was not loaded)."
                # ---------------------------------------------------------
                
            else:
                print("❌ فشل OpenCV في قراءة ملف الصورة الناتج.")
                ai_log_result = "❌ OpenCV failed to read captured image."
                
            # تنظيف النظام وحذف الملف المؤقت لحفظ مساحة الذاكرة
            os.remove(temp_filename)
        else:
            print("❌ لم يتم العثور على الملف المؤقت بعد التقاطه.")
            ai_log_result = "❌ Temporary image file not found."
            
    except subprocess.CalledProcessError as e:
        print(f"❌ فشل بايبلاين النظام في التقاط الصورة: {e}")
        ai_log_result = f"❌ Camera pipeline failed: {e}"
    except Exception as e:
        print(f"❌ حدث خطأ غير متوقع: {e}")
        ai_log_result = f"❌ Error: {e}"
        
    return ai_log_result  # نعيد النتيجة ليتم طباعتها في لوحة التحكم الرئيسية