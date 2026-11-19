
# استدعاء المكتبات المطلوبة
import streamlit as st
import json
import urllib.request
from pathlib import Path

# تحديد اسم ملف حفظ المحادثات
HISTORY_FILE = Path(__file__).with_name("chat_history.json")

# تحديد موديل الذكاء الاصطناعي
MODEL = "gemma3:270m"

# دالة تحميل المحادثات القديمة
def load_chat():
    if HISTORY_FILE.exists():
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as file:
                return json.load(file)
        except (json.JSONDecodeError, OSError):
            return []
    return []

# دالة حفظ المحادثات في ملف
def save_chat(messages):
    with open(HISTORY_FILE, "w", encoding="utf-8") as file:
        json.dump(messages, file, ensure_ascii=False, indent=4)

# دالة إرسال الرسائل إلى الذكاء الاصطناعي
def ask_ai(messages):
    data = {
        "model": MODEL,
        "messages": messages,
        "stream": False
    }

    # الاتصال بـ Ollama
    request = urllib.request.Request(
        "http://localhost:11434/api/chat",
        data=json.dumps(data).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )

    # استقبال رد الذكاء الاصطناعي
    with urllib.request.urlopen(request, timeout=120) as response:
        result = json.loads(response.read().decode("utf-8"))

    return result["message"]["content"]

# إعداد واجهة الشات
st.set_page_config(page_title="My AI Chat", page_icon="🤖")

st.title("🤖 My AI Chat")
st.caption("Your conversations are saved automatically.")

# تحميل المحادثات القديمة عند فتح التطبيق
if "messages" not in st.session_state:
    st.session_state.messages = load_chat()

# زر حذف المحادثات
if st.sidebar.button("🗑️ Clear Chat"):
    st.session_state.messages = []
    save_chat([])
    st.rerun()

# عرض جميع الرسائل القديمة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# استقبال رسالة جديدة من المستخدم
prompt = st.chat_input("Type your message...")

if prompt:
    # حفظ رسالة المستخدم
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    save_chat(st.session_state.messages)

    # عرض رسالة المستخدم
    with st.chat_message("user"):
        st.write(prompt)

    # إرسال المحادثة كاملة إلى الذكاء الاصطناعي
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                answer = ask_ai(st.session_state.messages)
            except Exception as error:
                answer = f"Error: {error}"

            st.write(answer)

    # حفظ رد الذكاء الاصطناعي
    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })

    save_chat(st.session_state.messages)




