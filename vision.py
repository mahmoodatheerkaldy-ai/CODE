import os
from ultralytics import YOLO
import cv2

# 1. تحميل الموديل
model = YOLO('best.pt')

# 2. تحديد مسار الصور (تأكد من مطابقة المسار في جهازك)
image_folder = r'data\test images'
output_folder = r'.\results'

# إنشاء مجلد للنتائج إذا لم يكن موجوداً
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

print("🔍 بدأ فحص الصور في المجلد...")

# 3. المرور على كل صورة في المجلد
for image_name in os.listdir(image_folder):
    if image_name.endswith(('.jpg', '.jpeg', '.png')):
        img_path = os.path.join(image_folder, image_name)
        
        # تشغيل الفحص
        results = model.predict(source=img_path, conf=0.3, save=False)
        
        # رسم النتائج وحفظ الصورة الناتجة
        res_plotted = results[0].plot()
        output_path = os.path.join(output_folder, f"res_{image_name}")
        cv2.imwrite(output_path, res_plotted)
        
        print(f"✅ تم فحص: {image_name}")
        print(model.names)

print(f"\n✨ انتهى الفحص! يمكنك مشاهدة النتائج في مجلد: {output_folder}")