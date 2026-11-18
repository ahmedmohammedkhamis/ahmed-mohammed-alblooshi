
# استدعاء المكتبات
import streamlit as st
import json
import urllib.request

# عنوان البرنامج
st.title("AI Chat")

# إنشاء ذاكرة لحفظ المحادثة
if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض المحادثات السابقة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# إنشاء مربع لكتابة السؤال
question = st.chat_input("Ask anything...")

# عند إرسال سؤال
if question:

    # حفظ سؤال المستخدم
    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    # عرض السؤال
    with st.chat_message("user"):
        st.write(question)

    # تجهيز المحادثة للذكاء الاصطناعي
    data = {
        "model": "gemma3:1b",
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a helpful assistant. "
                    "Remember the user's information. "
                    "Do not confuse the user's identity with yours. "
                    "Answer clearly and briefly."
                )
            }
        ] + st.session_state.messages,
        "stream": False
    }

    # تجهيز الاتصال مع Ollama
    request = urllib.request.Request(
        "http://localhost:11434/api/chat",
        data=json.dumps(data).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )

    # إرسال السؤال واستقبال الإجابة
    try:
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                with urllib.request.urlopen(
                    request, timeout=120
                ) as response:
                    result = json.loads(
                        response.read().decode("utf-8")
                    )

            # استخراج الإجابة وعرضها
            answer = result["message"]["content"]
            st.write(answer)

        # حفظ الإجابة في الذاكرة
        st.session_state.messages.append({
            "role": "assistant",
            "content": answer
        })

    # عرض الخطأ في حالة فشل الاتصال
    except Exception as error:
        st.error(str(error))
        st.session_state.messages.pop()

# زر مسح المحادثة
if st.sidebar.button("Clear Chat"):
    st.session_state.messages = []
    st.rerun()
