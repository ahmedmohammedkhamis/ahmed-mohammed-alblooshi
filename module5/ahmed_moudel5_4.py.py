
# استدعاء مكتبة JSON لتحويل البيانات
import json

# استدعاء أدوات الاتصال بالـ API
from urllib.request import Request, urlopen

# تحديد شخصية الذكاء الاصطناعي
system_prompt = "You are a Python teacher. Answer simply and briefly with important information."

# أخذ سؤال من المستخدم
question = input("Ask me: ")

# تجهيز البيانات لإرسالها إلى Ollama
data = {
    "model": "gemma3:270m",
    "messages": [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": question}
    ],
    "stream": False
}

# تجهيز الاتصال مع Ollama
request = Request(
    "http://localhost:11434/api/chat",
    data=json.dumps(data).encode("utf-8"),
    headers={"Content-Type": "application/json"}
)

# استقبال الإجابة وتحويلها إلى بيانات Python
with urlopen(request) as response:
    result = json.load(response)

# عرض إجابة الذكاء الاصطناعي
print("Teacher:", result["message"]["content"])
