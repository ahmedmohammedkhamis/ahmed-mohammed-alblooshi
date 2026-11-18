
# استدعاء مكتبة Streamlit لإنشاء واجهة المستخدم
import streamlit as st

# استدعاء المكتبات اللازمة للتواصل مع Ollama
import json
import urllib.request

# كتابة عنوان الصفحة
st.title("AI Chat")

# كتابة وصف بسيط
st.write("Ask the AI any question!")

# إنشاء مربع يكتب فيه المستخدم سؤاله
question = st.text_input("Enter your question:")

# إنشاء زر لإرسال السؤال
if st.button("Send"):

    # التأكد أن المستخدم كتب سؤالاً
    if question.strip():

        # تجهيز البيانات لإرسالها إلى الذكاء الاصطناعي
        data = {
            "model": "gemma3:270m",
            "messages": [
                {
                    "role": "system",
                    "content": "You are a helpful AI assistant."
                },
                {
                    "role": "user",
                    "content": question
                }
            ],
            "stream": False
        }

        # تحويل البيانات إلى JSON
        json_data = json.dumps(data).encode("utf-8")

        # تجهيز الطلب لإرساله إلى Ollama
        req = urllib.request.Request(
            "http://localhost:11434/api/chat",
            data=json_data,
            headers={"Content-Type": "application/json"}
        )

        # إرسال السؤال واستقبال الإجابة
        try:
            with urllib.request.urlopen(req) as response: 
                result = json.loads(response.read().decode("utf-8"))

            # استخراج إجابة الذكاء الاصطناعي
            answer = result["message"]["content"]

            # عرض الإجابة على الصفحة
            st.write("AI Answer:")
            st.write(answer)

        # عرض رسالة في حالة حدوث مشكلة
        except Exception as e:
            st.error(f"Error: {e}")

    else:
        st.warning("Please enter a question!")
