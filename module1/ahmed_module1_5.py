# إنشاء دالة تستقبل النص وسعر الحرف
def speaking(text, price):

    # متغير لحفظ النص الجديد
    shifted = ""

    # متغير لحساب عدد الحروف
    letters = 0

    # المرور على كل حرف في النص
    for char in text:

        # التأكد أن الحرف إنجليزي
        if "a" <= char <= "z" or "A" <= char <= "Z":

            # تبديل آخر حرف بأول حرف
            if char == "z":
                shifted += "a"

            elif char == "Z":
                shifted += "A"

            # تبديل الحرف بالحرف التالي
            else:
                shifted += chr(ord(char) + 1)

            # زيادة عدد الحروف
            letters += 1

        else:
            # ترك المسافات والرموز والأرقام كما هي
            shifted += char

    # إرجاع النتيجة على شكل قاموس
    return {
        "shifted_string": shifted,
        "word_count": len(text.split()),
        "price": letters * price
    }


# طلب النص من المستخدم
text = input("Enter text: ")

# طلب سعر الحرف من المستخدم
price = float(input("Enter letter price: "))

# تشغيل الدالة وعرض النتيجة
print(speaking(text, price))