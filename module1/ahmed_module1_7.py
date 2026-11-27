# إنشاء دالة تستقبل قيمة
def check_string(value):

    # محاولة تنفيذ الكود
    try:

        # التأكد أن القيمة من نوع نص
        if not isinstance(value, str):

            # إنشاء خطأ إذا لم تكن القيمة نصاً
            raise TypeError

        # إرجاع النص إذا كان صحيحاً
        return value

    # التعامل مع الخطأ
    except TypeError:

        # إرجاع قيمة فارغة
        return None


# تجربة الدالة باستخدام نص
print(check_string("Hello"))

# تجربة الدالة باستخدام رقم
print(check_string(123))