# نستدعي مكتبة MCP
from fastmcp import FastMCP

# نستدعي مكتبة الاتصال مع Ollama
import urllib.request

# نستدعي مكتبة التعامل مع البيانات
import json

# ننشئ سيرفر MCP
mcp = FastMCP("Ollama MCP")

# ننشئ أداة تستقبل سؤال المستخدم
@mcp.tool()
def ask_ollama(question: str):

    # نحدد الموديل والسؤال
    data = {
        "model": "gemma3:270m",
        "prompt": question,
        "stream": False
    }

    # نرسل السؤال إلى Ollama
    request = urllib.request.Request(
        "http://localhost:11434/api/generate",
        data=json.dumps(data).encode(),
        headers={"Content-Type": "application/json"}
    )

    # نستقبل إجابة الذكاء الاصطناعي
    response = urllib.request.urlopen(request)

    # نحول الإجابة إلى بيانات
    result = json.loads(response.read())

    # نرجع الإجابة إلى MCP Inspector
    return result["response"]

# نشغل سيرفر MCP
if __name__ == "__main__":
    mcp.run()