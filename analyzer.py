import matplotlib.pyplot as plt
import numpy as np
import random as rn

def analyze_moisture_levels(width, length, field_data=None):
    # 1. إعداد مساحة الرسم
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')

    # 2. إنشاء الشبكة بناءً على أبعاد المستخدم
    x = np.arange(width)
    y = np.arange(length)
    x_grid, y_grid = np.meshgrid(x, y)
    
    x_pos = x_grid.ravel()
    y_pos = y_grid.ravel()
    z_pos = np.zeros_like(x_pos)

    # 3. التعامل مع البيانات (الحقيقية أو التجريبية)
    if field_data is not None:
        # إذا قمت بتمرير قائمة بيانات حقيقية [x, y, value]
        # نحتاج للتأكد من مطابقتها لأبعاد الشبكة
        dz = np.array(field_data) 
    else:
        # بيانات تجريبية إذا لم تتوفر بيانات حقيقية (كما في صورتك)
        dz = np.random.rand(len(x_pos)) * 100 

    # 4. أبعاد الأعمدة (تغطية المتر المربع)
    dx = dy = 1

    # 5. الرسم
    # قمت بتغيير اللون إلى خريطة ألوان (Cmap) ليعطي مظهراً احترافياً
    colors = plt.cm.YlGnBu(dz / 100)
    ax.bar3d(x_pos, y_pos, z_pos, dx, dy, dz, color=colors, alpha=0.8)
    
    ax.set_box_aspect(width, length, 200)
    # 6. تسمية المحاور وتحديد النطاق
    ax.set_xlabel('Width (M)')
    ax.set_ylabel('Length (M)')
    ax.set_zlabel('Moisture %')
    ax.set_title(f'Field Moisture Map ({width}x{length}m)')
    
    # ضمان بقاء الرسم داخل حدود الحقل
    ax.set_xlim(0, width)
    ax.set_ylim(0, length)
    ax.set_zlim(0, 200)

    plt.show()

# --- طريقة الاستدعاء من قبل المستخدم ---
if __name__ == "__main__":
    user_w = int(input("أدخل عرض الحقل: "))
    user_l = int(input("أدخل طول الحقل: "))
    
    analyze_moisture_levels(user_w, user_l)
    
data_field = np.random.uniform(0, 100, size=(user_w * user_l))  
analyze_moisture_levels(user_w, user_l, field_data=data_field)