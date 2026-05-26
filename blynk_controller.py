import socket
import time

# استقبال البيانات على جميع الواجهات عبر المنفذ المحلي 5005
UDP_IP = "0.0.0.0"
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

print("⚡ [LOCAL SERVER] - تم تشغيل السيرفر المحلي بنجاح!")
print(f"📡 السيرفر يستمع الآن على المنفذ: {UDP_PORT} (بدون إنترنت 100%)")
print("✅ أرسل الأوامر الآن من اللابتوب لتحريك الروبوت...\n")

last_command = ""

try:
    while True:
        # استقبال الأمر (حجم الحزمة 1024 بايت)
        data, addr = sock.recvfrom(1024)
        command = data.decode('utf-8').strip().upper()
        
        if command != last_command:
            last_command = command
            
            if command == "FORWARD":
                print("🚀 [FORWARD] - تحريك الأرجل للأمام فورا")
            elif command == "BACKWARD":
                print("⬅️ [BACKWARD] - تحريك الأرجل للخلف فورا")
            elif command == "LEFT":
                print("↩️ [LEFT] - توجيه الروبوت يساراً")
            elif command == "RIGHT":
                print("↪️ [RIGHT] - توجيه الروبوت يمينا")
            elif command == "STOP":
                print("🛑 [STOP] - إيقاف الحركة كلياً")
                
except KeyboardInterrupt:
    print("\n🛑 تم إيقاف السيرفر المحلي.")
finally:
    sock.close()