# استدعاء مكتبة قاعدة البيانات
import sqlite3

# استدعاء FastAPI
from fastapi import FastAPI

# إنشاء التطبيق
app = FastAPI()

# إنشاء رابط لإضافة البيانات
@app.post("/insert")
def insert_data():

    # الاتصال بقاعدة البيانات
    conn = sqlite3.connect("tasks.db")

    # إنشاء أداة لتنفيذ أوامر SQL
    cursor = conn.cursor()

    # إضافة الصف الأول
    cursor.execute("""
        INSERT INTO tasks (title, description, status)
        VALUES ('Study English', 'Learn English', 'pending')
    """)

    # إضافة الصف الثاني
    cursor.execute("""
        INSERT INTO tasks (title, description, status)
        VALUES ('Study Math', 'Learn Math', 'pending')
    """)

    # حفظ البيانات
    conn.commit()

    # إغلاق الاتصال
    conn.close()

    # عرض رسالة نجاح
    return {"message": "2 rows added successfully"}