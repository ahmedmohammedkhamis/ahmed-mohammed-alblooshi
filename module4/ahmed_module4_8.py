# استدعاء مكتبة قاعدة البيانات
import sqlite3

# إنشاء دالة البحث
def search_data(word):

    # الاتصال بقاعدة البيانات
    conn = sqlite3.connect("tasks.db")

    # إنشاء أداة لتنفيذ الأوامر
    cursor = conn.cursor()

    # البحث داخل عمود description فقط
    cursor.execute("""
        SELECT * FROM tasks
        WHERE description LIKE ?
    """, ("%" + word + "%",))

    # جلب نتائج البحث
    rows = cursor.fetchall()

    # إغلاق الاتصال
    conn.close()

    # إرجاع نتائج البحث
    return rows

# سؤال المستخدم عن الكلمة المطلوبة
word = input("Enter search: ")

# استدعاء دالة البحث
results = search_data(word)

# التأكد من وجود نتائج
if results:

    # طباعة النتائج
    for row in results:
        print(row)

# في حال عدم وجود نتائج
else:
    print("No results found")