# إنشاء دالة لحساب عدد كلمات العناوين
def count_address():

    # فتح الملف للقراءة
    with open("address.text", "r", encoding="utf-8") as file:

        # قراءة جميع الأسطر
        lines = file.readlines()

    # فتح نفس الملف لإضافة النتائج
    with open("address.text", "a", encoding="utf-8") as file:

        # المرور على جميع الأسطر
        for line in lines:

            # البحث عن السطر الذي يبدأ بكلمة Address
            if line.startswith("Address:"):

                # إزالة كلمة Address من السطر
                address = line.replace("Address:", "", 1).strip()

                # حساب عدد الكلمات
                count = len(address.split())

                # إضافة النتيجة إلى الملف
                file.write(f"\n{address}: Word count = {count}\n")

                # عرض النتيجة
                print(address, count)


# تشغيل الدالة
count_address()