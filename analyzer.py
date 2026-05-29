import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def plot_moisture_3d(moisture_map, min_moisture):
    """
    يقوم برسم مخطط ثلاثي الأبعاد يوضح مستويات الرطوبة في الحقل.
    
    :param moisture_map: مصفوفة ثنائية الأبعاد تحتوي على قيم الرطوبة المستلمة من الروبوت.
    :param min_moisture: الحد الأدنى للرطوبة الطبيعية (Threshold).
    """
    # تحويل المصفوفة إلى numpy array للتعامل مع الأبعاد بسهولة
    data = np.array(moisture_map)
    rows, steps = data.shape

    # إنشاء الإحداثيات شبكية للمحاور X و Y
    x_pos, y_pos = np.meshgrid(np.arange(rows), np.arange(steps), indexing='ij')
    
    # تحويل الإحداثيات إلى مصفوفة أحادية البعد ليقبلها رسم الأعمدة 3D
    x_pos = x_pos.ravel()
    y_pos = y_pos.ravel()
    z_pos = np.zeros_like(x_pos) # قاعدة الأعمدة تبدأ من الصفر

    # تحديد أبعاد قاعدة كل عمود (سمك العمود في الرسم)
    dx = dy = 0.5 
    dz = data.ravel() # ارتفاع العمود يمثل قيمة الرطوبة

    # تحديد ألوان الأعمدة بناءً على الحد الأدنى (أخضر للممتاز، أحمر للإنذار)
    colors = []
    for val in dz:
        if val < min_moisture:
            colors.append('#e74c3c') # لون أحمر للرطوبة المنخفضة
        else:
            colors.append('#2ecc71') # لون أخضر للرطوبة الطبيعية

    # إنشاء النافذة والرسم ثلاثي الأبعاد
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    # رسم الأعمدة ثلاثية الأبعاد
    bars = ax.bar3d(x_pos, y_pos, z_pos, dx, dy, dz, color=colors, zsort='average', edgecolor='black', linewidth=0.5)

    # تسمية المحاور والعناوين
    ax.set_xlabel('Rows (Lines)', fontsize=12, labelpad=10)
    ax.set_ylabel('Steps per Row', fontsize=12, labelpad=10)
    ax.set_zlabel('Moisture Level (%)', fontsize=12, labelpad=10)
    ax.set_title(f'📊 Specter 3D Soil Moisture Field Map\n(Threshold: {min_moisture}%)', fontsize=14, fontweight='bold', pad=20)

    # ضبط أرقام المؤشرات على المحاور لتبدأ من 1 بدلاً من 0 لتسهيل القراءة
    ax.set_xticks(np.arange(rows))
    ax.set_xticklabels([f"Row {i+1}" for i in range(rows)])
    ax.set_yticks(np.arange(steps))
    ax.set_yticklabels([f"Step {i+1}" for i in range(steps)])

    # إضافة وسيلة إيضاح (Legend) يدوية للألوان
    from matplotlib.lines import Line2D
    legend_elements = [
        Line2D([0], [0], marker='o', color='w', label='Normal Moisture', markerfacecolor='#2ecc71', markersize=10),
        Line2D([0], [0], marker='o', color='w', label='Low Moisture (Alert)', markerfacecolor='#e74c3c', markersize=10)
    ]
    ax.legend(handles=legend_elements, loc='upper left')

    # تفعيل إمكانية تدوير الرسم بالماوس واستعراضه
    plt.savefig('moisture_3d_map.png', dpi=300, bbox_inches='tight')
    print("💾 [SUCCESS] 3D Diagram has been saved as 'moisture_3d_map.png' in your CODE folder!")
    plt.close()

# --- جزء تجريبي للاختبار الفردي ---
# إذا قمت بتشغيل هذا الملف مباشرة، سيقوم بتوليد بيانات وهمية لترى شكل الرسم
if __name__ == "__main__":
    print("⏳ Running test analysis with sample data...")
    # حقل وهمي بأبعاد 3 خطوط × 5 خطوات
    sample_map = [
        [28.5, 32.1, 15.4, 29.0, 31.2],  # الخط الأول (لاحظ الـ 15.4 ستظهر حمراء)
        [12.0, 26.4, 30.1, 11.5, 27.8],  # الخط الثاني
        [34.0, 35.5, 29.9, 33.1, 30.5]   # الخط الثالث (كله أخضر)
    ]
    sample_threshold = 20.0 # الحد الأدنى
    
    plot_moisture_3d(sample_map, sample_threshold)