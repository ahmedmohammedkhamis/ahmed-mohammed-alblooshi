
# استدعاء أداة إنشاء Agents من LangChain
from langchain.agents import create_agent

# استدعاء أداة تعريف الدوال كأدوات
from langchain_core.tools import tool

# استدعاء موديل الذكاء الاصطناعي
from langchain_ollama import ChatOllama

# استدعاء نوع الرسالة لمعرفة الأدوات المستخدمة
from langchain_core.messages import ToolMessage


# إنشاء أداة الجمع
@tool
def add(a: float, b: float) -> float:
    """Add two numbers."""
    return a + b


# إنشاء أداة الطرح
@tool
def subtract(a: float, b: float) -> float:
    """Subtract the second number from the first."""
    return a - b


# إنشاء أداة الضرب
@tool
def multiply(a: float, b: float) -> float:
    """Multiply two numbers."""
    return a * b


# إنشاء أداة القسمة
@tool
def divide(a: float, b: float) -> str:
    """Divide the first number by the second."""

    # منع القسمة على صفر
    if b == 0:
        return "Error: Cannot divide by zero"

    # إرجاع الناتج
    return str(a / b)


# إنشاء دالة لتجهيز Agent الأول
def create_math_agent(model):

    # إنشاء Agent متخصص في الحساب
    agent = create_agent(
        model=model,
        tools=[add, subtract, multiply, divide],
        system_prompt=(
            "You are a math agent. "
            "Always use math tools to calculate. "
            "Give the final result clearly."
        )
    )

    # إرجاع Agent الأول
    return agent


# إنشاء دالة لتجهيز Agent الثاني
def create_review_agent(model):

    # إنشاء Agent مستقل لمراجعة الحساب
    agent = create_agent(
        model=model,
        tools=[add, subtract, multiply, divide],
        system_prompt=(
            "You are a math review agent. "
            "Receive the original question and first agent answer. "
            "Independently check the calculation using tools. "
            "Say Verified if correct. "
            "If incorrect, explain and give the correct result. "
            "Keep your review short."
        )
    )

    # إرجاع Agent الثاني
    return agent


# إنشاء دالة لتشغيل Agentين بالتسلسل
def run_multi_agent(math_agent, review_agent, question):

    # إرسال سؤال المستخدم إلى Agent الأول
    first_result = math_agent.invoke({
        "messages": [
            {"role": "user", "content": question}
        ]
    })

    # استخراج الإجابة النهائية من Agent الأول
    first_answer = first_result["messages"][-1].content

    # عرض إجابة Agent الأول
    print("\nAgent 1 - Math:")
    print(first_answer)

    # عرض أدوات الحساب المستخدمة فعلياً
    for message in first_result["messages"]:
        if isinstance(message, ToolMessage):
            print("Math tool:", message.name)
            print("Tool result:", message.content)

    # تجهيز السؤال والنتيجة لإرسالهما إلى Agent الثاني
    review_input = (
        f"Original question: {question}\n"
        f"First agent answer: {first_answer}\n"
        "Check this answer independently using math tools."
    )

    # إرسال نتيجة Agent الأول إلى Agent الثاني
    second_result = review_agent.invoke({
        "messages": [
            {"role": "user", "content": review_input}
        ]
    })

    # استخراج مراجعة Agent الثاني
    review_answer = second_result["messages"][-1].content

    # عرض نتيجة المراجعة
    print("\nAgent 2 - Review:")
    print(review_answer)

    # عرض أدوات المراجعة المستخدمة فعلياً
    used_tool = False

    for message in second_result["messages"]:
        if isinstance(message, ToolMessage):
            used_tool = True
            print("Review tool:", message.name)
            print("Tool result:", message.content)

    # تنبيه إذا لم يستخدم Agent الثاني أداة للتحقق
    if not used_tool:
        print("Note: Review agent did not use a math tool.")

    # إرجاع إجابة الحساب والمراجعة
    return first_answer, review_answer


# إنشاء دالة التشغيل الرئيسية
def main():

    # اختيار موديل الذكاء الاصطناعي
    model = ChatOllama(
        model="qwen2.5:3b",
        temperature=0
    )

    # تجهيز Agent الأول للحساب
    math_agent = create_math_agent(model)

    # تجهيز Agent الثاني للمراجعة
    review_agent = create_review_agent(model)

    # عرض رسالة بدء البرنامج
    print("Multi Agent Math System")

    # تكرار استقبال أسئلة المستخدم
    while True:

        # طلب العملية الحسابية
        question = input("\nEnter math question (or exit): ")

        # إنهاء البرنامج عند كتابة exit
        if question.lower() == "exit":
            break

        # تشغيل Agent الأول ثم Agent الثاني
        try:
            run_multi_agent(math_agent, review_agent, question)

        # عرض الخطأ إذا حدثت مشكلة
        except Exception as error:
            print("Error:", error)


# بدء تشغيل البرنامج
if __name__ == "__main__":
    main()
