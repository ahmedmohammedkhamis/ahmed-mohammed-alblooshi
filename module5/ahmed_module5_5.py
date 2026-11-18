
# استدعاء المكتبة للتواصل مع نموذج الذكاء الاصطناعي
import ollama

# نطلب من المستخدم كتابة سؤال
question = input("Ask me anything: ")

# إرسال السؤال إلى نموذج الذكاء الاصطناعي
response = ollama.chat(
    model="llama3.2",
    messages=[
        {"role": "user", "content": question}
    ],
    options={
        # زيادة حجم نافذة السياق
        "num_ctx": 8192,

        # التحكم في إبداع الإجابات
        "temperature": 0.7
    }
)

# عرض إجابة الذكاء الاصطناعي
print(response["message"]["content"])
