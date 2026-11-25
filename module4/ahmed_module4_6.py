# استدعاء مكتبة قاعدة البيانات
import sqlite3

# الاتصال بقاعدة البيانات السابقة
conn = sqlite3.connect("tasks.db")

# إنشاء أداة لتنفيذ أوامر SQL
cursor = conn.cursor()

# إضافة عمود جديد إلى الجدول
cursor.execute("""
    ALTER TABLE tasks
    ADD COLUMN missing_field TEXT
""")

# وضع حرف عشوائي في العمود الجديد لكل صف
cursor.execute("""
    UPDATE tasks
    SET missing_field = CHAR(65 + ABS(RANDOM() % 26))
""")

# حفظ التغييرات
conn.commit()

# عرض البيانات بعد التعديل
cursor.execute("SELECT * FROM tasks")

# طباعة جميع الصفوف
for row in cursor.fetchall():
    print(row)

# إغلاق الاتصال بقاعدة البيانات
conn.close()