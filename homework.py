import matplotlib.pyplot as plt
import numpy as np

# 1. إدخال البيانات من ورقتك
# الجهد (V)
voltage = np.array([0, 5, 10, 15, 20, 25, 30])
# التيار (I) بالامبير
current = np.array([0, 0, 0.022, 0.034, 0.045, 0.057, 0.068])

# 2. حساب أفضل خط تناسب (Linear Regression) 
# سنستخدم القراءات من 10 فولت فما فوق لأنها تمثل منطقة العمل الخطية
mask = voltage >= 10
m, b = np.polyfit(current[mask], voltage[mask], 1)

# 3. إعداد الرسم البياني
plt.figure(figsize=(8, 6))
plt.scatter(current, voltage, color='red', label='Experimental Data (Points)')
plt.plot(current[mask], m*current[mask] + b, color='blue', linestyle='--', 
         label=f'Linear Fit (R = {m:.2f} Ω)')

# 4. إضافة العناوين والتنسيق
plt.title("Verification of Ohm's Law", fontsize=14)
plt.xlabel('Current (I) [Amperes]', fontsize=12)
plt.ylabel('Voltage (V) [Volts]', fontsize=12)
plt.grid(True, linestyle=':', alpha=0.7)
plt.legend()

# إضافة نص يوضح قيمة المقاومة المحسوبة برمجياً
plt.text(0.01, 25, f'Calculated R: {m:.2f} Ω', fontsize=12, 
         bbox=dict(facecolor='white', alpha=0.5))

# 5. عرض الرسم
plt.show()