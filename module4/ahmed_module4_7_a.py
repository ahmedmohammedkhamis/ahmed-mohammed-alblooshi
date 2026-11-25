# استدعاء مكتبة قاعدة البيانات
import sqlite3

# الاتصال بقاعدة البيانات
conn = sqlite3.connect("tasks.db")

# إنشاء أداة لتنفيذ الأوامر
cursor = conn.cursor()

# ترتيب البيانات حسب الحروف
cursor.execute("""
    SELECT * FROM tasks
    ORDER BY missing_field ASC
""")

# جلب جميع البيانات
rows = cursor.fetchall()

# طباعة البيانات بعد الترتيب
for row in rows:
    print(row)

# إغلاق الاتصال
conn.close()