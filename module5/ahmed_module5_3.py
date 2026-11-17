
# استيراد الأدوات اللازمة للاتصال بـ Ollama
import json
from urllib.request import Request, urlopen

# سؤال المستخدم
question = input("Ask Ollama: ")

# تجهيز السؤال والموديل
data = {
    "model": "gemma3:270m",
    "prompt": question,
    "stream": False
}

# إرسال السؤال إلى Ollama API
request = Request(
    "http://localhost:11434/api/generate",
    data=json.dumps(data).encode(),
    headers={"Content-Type": "application/json"}
)

# استقبال وطباعة الإجابة
with urlopen(request) as response:
    result = json.load(response)

print("Ollama:", result["response"])
