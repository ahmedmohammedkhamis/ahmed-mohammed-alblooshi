# استدعاء مكتبة قاعدة البيانات
import sqlite3

# الاتصال بقاعدة البيانات
conn = sqlite3.connect("tasks.db")

# إنشاء أداة لتنفيذ الأوامر
cursor = conn.cursor()

# جلب جميع البيانات من الجدول
cursor.execute("SELECT * FROM tasks")

# تخزين البيانات في قائمة
rows = cursor.fetchall()

# ترتيب البيانات حسب العمود الأخير
rows.sort(key=lambda row: row[-1] or "")

# طباعة البيانات بعد الترتيب
for row in rows:
    print(row)

# إغلاق الاتصال
conn.close()