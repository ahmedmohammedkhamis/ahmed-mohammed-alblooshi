
# استدعاء مكتبة قراءة ملفات Word
from langchain_community.document_loaders import UnstructuredWordDocumentLoader

# استدعاء أداة تقسيم النصوص
from langchain_text_splitters import RecursiveCharacterTextSplitter

# استدعاء موديل تحويل النصوص إلى أرقام
from langchain_ollama import OllamaEmbeddings

# استدعاء أداة تخزين المعلومات والبحث فيها
from langchain_core.vectorstores import InMemoryVectorStore

# استدعاء أداة التحقق من وجود الملف
from pathlib import Path


# إنشاء دالة تستقبل مكان الملف والسؤال
def read_word(file_path, question):

    # تحديد ملف Word المطلوب
    loader = UnstructuredWordDocumentLoader(file_path)

    # قراءة المعلومات الموجودة داخل الملف
    documents = loader.load()

    # إنشاء أداة تقسيم النصوص
    splitter = RecursiveCharacterTextSplitter(
        # تقسيم النص إلى أجزاء أصغر للحصول على نتائج أكثر
chunk_size=50,
chunk_overlap=10
    )

    # تقسيم محتوى الملف إلى أجزاء صغيرة
    chunks = splitter.split_documents(documents)

    # اختيار موديل تحويل النصوص إلى أرقام
    embeddings = OllamaEmbeddings(
        model="nomic-embed-text"
    )

    # تخزين الأجزاء في الذاكرة للبحث فيها
    database = InMemoryVectorStore.from_documents(
        chunks,
        embedding=embeddings
    )

    # البحث عن أفضل 3 أجزاء مرتبطة بالسؤال
    results = database.similarity_search(question, k=3)

    # إرجاع النتائج
    return results


# طلب مكان ملف Word من المستخدم
file_path = input("Enter Word file path: ").strip().strip('"').strip("'")

# التأكد من وجود الملف قبل المتابعة
if not Path(file_path).is_file():
    print("File not found! Check your Word file path.")

else:
    # طلب السؤال من المستخدم
    question = input("Enter your question: ")

    # تشغيل دالة البحث وتخزين النتائج
    results = read_word(file_path, question)

    # المرور على نتائج البحث وعرضها
    for number, document in enumerate(results, start=1):

        # طباعة رقم النتيجة
        print(f"\nResult {number}:")

        # طباعة محتوى النتيجة
        print(document.page_content)
