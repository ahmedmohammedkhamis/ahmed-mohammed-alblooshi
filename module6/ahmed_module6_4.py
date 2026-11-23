
# استدعاء أداة إنشاء Agent من LangChain
from langchain.agents import create_agent

# استدعاء أداة تعريف الدوال كأدوات للذكاء الاصطناعي
from langchain_core.tools import tool

# استدعاء موديل Ollama
from langchain_ollama import ChatOllama

# استدعاء نوع الرسالة لمعرفة الأدوات المستخدمة
from langchain_core.messages import ToolMessage


# إنشاء أداة الجمع
@tool
def add(a: float, b: float) -> float:
    """Add two numbers together."""
    return a + b


# إنشاء أداة الطرح
@tool
def subtract(a: float, b: float) -> float:
    """Subtract the second number from the first."""
    return a - b


# إنشاء أداة الضرب
@tool
def multiply(a: float, b: float) -> float:
    """Multiply two numbers together."""
    return a * b


# إنشاء أداة القسمة
@tool
def divide(a: float, b: float) -> str:
    """Divide the first number by the second."""

    # التأكد أن الرقم الثاني ليس صفراً
    if b == 0:
        return "Error: Cannot divide by zero"

    # إرجاع نتيجة القسمة
    return str(a / b)


# إنشاء دالة لتجهيز Agent
def create_math_agent():

    # اختيار موديل الذكاء الاصطناعي
    model = ChatOllama(
        model="qwen2.5:3b",
        temperature=0
    )

    # إنشاء Agent وتزويده بالأدوات الحسابية
    agent = create_agent(
        model=model,
        tools=[add, subtract, multiply, divide],
        system_prompt=(
            "You are a math assistant. "
            "Always use the provided tools for calculations. "
            "Answer clearly and briefly."
        )
    )

    # إرجاع Agent
    return agent


# إنشاء دالة تسأل Agent وتعرض الإجابة
def ask_agent(agent, question):

    # إرسال السؤال إلى Agent
    result = agent.invoke({
        "messages": [
            {"role": "user", "content": question}
        ]
    })

    # عرض الأدوات التي استخدمها Agent فعلياً
    for message in result["messages"]:

        # التأكد أن الرسالة نتيجة أداة
        if isinstance(message, ToolMessage):
            print("Tool used:", message.name)
            print("Tool result:", message.content)

    # إرجاع الإجابة النهائية
    return result["messages"][-1].content


# تشغيل البرنامج
if __name__ == "__main__":

    # تجهيز Agent
    agent = create_math_agent()

    # إبقاء البرنامج شغالاً لاستقبال الأسئلة
    while True:

        # طلب سؤال من المستخدم
        question = input("\nEnter math question (or exit): ")

        # إغلاق البرنامج إذا كتب المستخدم exit
        if question.lower() == "exit":
            break

        # إرسال السؤال وعرض الإجابة
        try:
            answer = ask_agent(agent, question)
            print("AI Answer:", answer)

        # إظهار الخطأ إذا فشل التنفيذ
        except Exception as error:
            print("Error:", error)
