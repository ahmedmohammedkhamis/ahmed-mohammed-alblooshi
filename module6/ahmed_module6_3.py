
# استدعاء مكتبة إنشاء واجهة الشات
import streamlit as st

# استدعاء مكتبة قواعد البيانات
import sqlite3

# استدعاء مكتبات الاتصال بالذكاء الاصطناعي
import json
import urllib.request

# استدعاء مكتبة التعامل مع مسارات الملفات
from pathlib import Path


# اختيار موديل الذكاء الاصطناعي
MODEL = "gemma3:1b"

# تحديد مكان قاعدة البيانات خارج مجلد التسليم
DB_FILE = Path(__file__).resolve().parent.parent / "module6_chat.db"


# إنشاء دالة لإنشاء قاعدة البيانات
def create_database():

    # الاتصال بقاعدة البيانات أو إنشاؤها
    connection = sqlite3.connect(DB_FILE)

    # إنشاء جدول المحادثات إذا لم يكن موجوداً
    connection.execute("""
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT NOT NULL,
            answer TEXT NOT NULL
        )
    """)

    # حفظ التعديلات
    connection.commit()

    # إغلاق الاتصال
    connection.close()


# إنشاء دالة لحفظ السؤال والجواب
def save_chat(question, answer):

    # فتح قاعدة البيانات
    connection = sqlite3.connect(DB_FILE)

    # إضافة السؤال والجواب داخل الجدول كنصوص
    connection.execute(
        "INSERT INTO chat_history (question, answer) VALUES (?, ?)",
        (question, answer)
    )

    # حفظ البيانات
    connection.commit()

    # إغلاق الاتصال
    connection.close()


# إنشاء دالة لقراءة المحادثات القديمة
def load_chat():

    # فتح قاعدة البيانات
    connection = sqlite3.connect(DB_FILE)

    # جلب الأسئلة والأجوبة بالترتيب
    rows = connection.execute(
        "SELECT question, answer FROM chat_history ORDER BY id"
    ).fetchall()

    # إغلاق الاتصال
    connection.close()

    # إرجاع المحادثات
    return rows


# إنشاء دالة للتواصل مع الذكاء الاصطناعي
def ask_ai(question):

    # إنشاء قائمة الرسائل
    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant. Answer briefly."
        }
    ]

    # قراءة آخر 5 محادثات من قاعدة البيانات
    history = load_chat()[-5:]

    # إضافة المحادثات السابقة حتى يتذكر السياق
    for old_question, old_answer in history:
        messages.append({
            "role": "user",
            "content": old_question
        })
        messages.append({
            "role": "assistant",
            "content": old_answer
        })

    # إضافة السؤال الجديد
    messages.append({
        "role": "user",
        "content": question
    })

    # تجهيز البيانات لإرسالها إلى Ollama
    data = {
        "model": MODEL,
        "messages": messages,
        "stream": False
    }

    # تجهيز طلب الاتصال
    request = urllib.request.Request(
        "http://localhost:11434/api/chat",
        data=json.dumps(data).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )

    # إرسال السؤال واستقبال الإجابة
    with urllib.request.urlopen(request, timeout=120) as response:
        result = json.loads(response.read().decode("utf-8"))

    # إرجاع إجابة الذكاء الاصطناعي
    return result["message"]["content"]


# تشغيل دالة تجهيز قاعدة البيانات
create_database()

# إعداد صفحة الشات
st.set_page_config(page_title="AHMED AI CHAT", page_icon="🤖")

# عرض عنوان البرنامج
st.title("AHMED AI CHAT")

# عرض وصف البرنامج
st.write("Chat with AI - Messages saved in SQLite")


# إنشاء زر لمسح المحادثات
if st.sidebar.button("Clear Chat"):

    # فتح قاعدة البيانات
    connection = sqlite3.connect(DB_FILE)

    # حذف المحادثات المحفوظة
    connection.execute("DELETE FROM chat_history")

    # حفظ التعديل وإغلاق الاتصال
    connection.commit()
    connection.close()

    # تحديث الصفحة
    st.rerun()


# عرض المحادثات المحفوظة من قاعدة البيانات
for old_question, old_answer in load_chat():

    # عرض سؤال المستخدم
    with st.chat_message("user"):
        st.write(old_question)

    # عرض جواب الذكاء الاصطناعي
    with st.chat_message("assistant"):
        st.write(old_answer)


# إنشاء مربع لكتابة السؤال
question = st.chat_input("Ask anything...")


# التأكد أن المستخدم كتب سؤالاً
if question:

    # عرض السؤال
    with st.chat_message("user"):
        st.write(question)

    # عرض إجابة الذكاء الاصطناعي
    with st.chat_message("assistant"):

        try:
            # إظهار رسالة أثناء تجهيز الإجابة
            with st.spinner("Thinking..."):

                # إرسال السؤال إلى الذكاء الاصطناعي
                answer = ask_ai(question)

                # حفظ السؤال والجواب في SQLite
                save_chat(question, answer)

            # عرض الإجابة
            st.write(answer)

        # إظهار الخطأ إذا فشل الاتصال
        except Exception as error:
            st.error(str(error))
