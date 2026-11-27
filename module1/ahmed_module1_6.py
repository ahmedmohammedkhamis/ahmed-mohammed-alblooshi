# إنشاء كلاس لحفظ معلومات الشخص
class Person:

    # تحديد المعلومات المطلوبة
    def __init__(self, name, contact, address, phone):
        self.name = name
        self.contact = contact
        self.address = address
        self.phone = phone

    # إنشاء دالة لحفظ المعلومات في ملف
    def save(self):

        # فتح ملف نصي لحفظ المعلومات
        with open("address.text", "a", encoding="utf-8") as file:

            # كتابة معلومات الشخص داخل الملف
            file.write(f"Name: {self.name}\n")
            file.write(f"Contact: {self.contact}\n")
            file.write(f"Address: {self.address}\n")
            file.write(f"Phone: {self.phone}\n")
            file.write("----------------\n")


# إنشاء دالة لإدخال معلومات الشخص
def main():

    # طلب المعلومات من المستخدم
    name = input("Enter name: ")
    contact = input("Enter contact: ")
    address = input("Enter address: ")
    phone = input("Enter phone number: ")

    # إرسال المعلومات إلى الكلاس
    person = Person(name, contact, address, phone)

    # تشغيل دالة الحفظ
    person.save()

    # عرض رسالة نجاح الحفظ
    print("Information saved successfully!")


# تشغيل البرنامج
main()