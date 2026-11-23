
# استدعاء مكتبة واجهة المستخدم
import streamlit as st

# استدعاء مكتبة قواعد البيانات
import sqlite3

# استدعاء مكتبات الاتصال مع Ollama
import json
import urllib.request

# استدعاء مكتبة تحديد مسار الملفات
from pathlib import Path

# استدعاء Pydantic للتحقق من البيانات
from pydantic import BaseModel, Field, ValidationError


# تحديد موديل الذكاء الاصطناعي
MODEL = "gemma3:1b"

# حفظ قاعدة البيانات خارج مجلد التسليم
DB_FILE = Path(__file__).resolve().parent.parent / "module6_pydantic.db"


# إنشاء نموذج Pydantic للمعلومات
class UserInfo(BaseModel):

    # الاسم إلزامي ولا يقبل نصاً فارغاً
    name: str = Field(min_length=1)

    # الوقت اختياري
    time: str | None = None

    # الرقم اختياري
    number: str | None = None


# إنشاء دالة لتجهيز قاعدة البيانات
def create_database():

    # فتح قاعدة البيانات أو إنشاؤها
    db = sqlite3.connect(DB_FILE)

    # إنشاء جدول لحفظ الأسئلة والأجوبة والمعلومات
    db.execute("""
        CREATE TABLE IF NOT EXISTS records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            user_data TEXT NOT NULL
        )
    """)

    # حفظ الجدول وإغلاق الاتصال
    db.commit()
    db.close()


# إنشاء دالة لحفظ النتائج في SQLite
def save_result(question, answer, user_info):

    # فتح قاعدة البيانات
    db = sqlite3.connect(DB_FILE)

    # تحويل معلومات Pydantic إلى نص JSON
    pydantic_json = user_info.model_dump_json()

    # حفظ السؤال والجواب والمعلومات
    db.execute(
        """
        INSERT INTO records (question, answer, user_data)
        VALUES (?, ?, ?)
        """,
        (question, answer, pydantic_json)
    )

    # حفظ التعديلات وإغلاق الاتصال
    db.commit()
    db.close()


# إنشاء دالة لقراءة المحادثات المحفوظة
def load_results():

    # فتح قاعدة البيانات
    db = sqlite3.connect(DB_FILE)

    # قراءة آخر 10 محادثات
    rows = db.execute(
        """
        SELECT question, answer, user_data
        FROM records
        ORDER BY id DESC
        LIMIT 10
        """
    ).fetchall()

    # إغلاق الاتصال وإرجاع النتائج
    db.close()
    return rows


# إنشاء دالة لإرسال السؤال إلى Ollama
def ask_ai(question, user_info):

    # تجهيز معلومات المستخدم للذكاء الاصطناعي
    user_message = (
        f"Name: {user_info.name}\n"
        f"Time: {user_info.time or 'Not provided'}\n"
        f"Number: {user_info.number or 'Not provided'}\n"
        f"Question: {question}"
    )

    # تجهيز البيانات المطلوبة من Ollama
    data = {
        "model": MODEL,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a helpful assistant. "
                    "Answer the user's question clearly and briefly. "
                    "Do not invent missing personal information."
                )
            },
            {
                "role": "user",
                "content": user_message
            }
        ],
        "stream": False
    }

    # تجهيز طلب الاتصال مع Ollama
    request = urllib.request.Request(
        "http://localhost:11434/api/chat",
        data=json.dumps(data).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )

    # إرسال السؤال واستقبال إجابة الذكاء الاصطناعي
    with urllib.request.urlopen(
        request, timeout=120
    ) as response:

        # قراءة جواب Ollama
        result = json.loads(
            response.read().decode("utf-8")
        )

    # إرجاع الإجابة كنص
    return result["message"]["content"]


# إنشاء قاعدة البيانات عند تشغيل البرنامج
create_database()


# إعداد صفحة Streamlit
st.set_page_config(
    page_title="AHMED AI CHAT",
    page_icon="🤖"
)

# عرض عنوان البرنامج
st.title("AHMED AI CHAT")

# شرح بسيط للمستخدم
st.write("Pydantic + LLM + SQLite")
st.write("Enter your information and ask a question.")


# إنشاء خانة الاسم الإلزامية
name = st.text_input("Name (required)")

# إنشاء خانة الوقت الاختيارية
time = st.text_input("Time (optional)")

# إنشاء خانة الرقم الاختيارية
number = st.text_input("Number (optional)")


# إنشاء مربع كتابة السؤال
question = st.chat_input("Ask your question...")


# التأكد أن المستخدم أرسل سؤالاً
if question:

    # عرض سؤال المستخدم
    with st.chat_message("user"):
        st.write(question)

    try:
        # التحقق من المعلومات باستخدام Pydantic
        user_info = UserInfo(
            name=name.strip(),
            time=time.strip() or None,
            number=number.strip() or None
        )

        # طلب الإجابة من الذكاء الاصطناعي
        with st.spinner("Thinking..."):
            answer = ask_ai(question, user_info)

        # حفظ النتيجة في SQLite
        save_result(question, answer, user_info)

        # عرض جواب الذكاء الاصطناعي
        with st.chat_message("assistant"):
            st.write(answer)

        # عرض البيانات المنظمة بصيغة Pydantic
        st.subheader("Structured Data")
        st.json(user_info.model_dump())

        # إظهار رسالة نجاح الحفظ
        st.success("Data saved to SQLite successfully!")

    # إظهار خطأ إذا كان الاسم مفقوداً
    except ValidationError:
        st.error("Please enter your name. Name is required.")

    # إظهار خطأ إذا فشل الاتصال أو الحفظ
    except Exception as error:
        st.error(str(error))


# إنشاء قسم لعرض المحادثات المحفوظة
with st.expander("Saved Records in SQLite"):

    # قراءة البيانات المحفوظة
    saved_rows = load_results()

    # عرض كل محادثة مع بياناتها
    for old_question, old_answer, old_data in saved_rows:

        # عرض السؤال القديم
        st.write("Question:", old_question)

        # عرض الإجابة المحفوظة
        st.write("Answer:", old_answer)

        # تحويل JSON المحفوظ إلى بيانات قابلة للعرض
        st.json(json.loads(old_data))

        # فاصل بين المحادثات
        st.divider()
