
# ==================================
# 1. إعدادات اللعبة الأساسية
# ==================================

# إنشاء لوحة 4 صفوف و4 أعمدة
# الصفر يعني المربع فاضي
board = [[0] * 4 for i in range(4)]

# نقاط اللاعب
score = 0

# رقم نستخدمه لتوليد أرقام شبه عشوائية
seed = 12345


# ==================================
# 2. توليد رقم شبه عشوائي
# ==================================

def random_number(n):
    global seed

    # تغيير قيمة seed للحصول على رقم جديد
    seed = (seed * 1103515245 + 12345) % 2147483648

    # إرجاع رقم من 0 إلى n-1
    return seed % n


# ==================================
# 3. إضافة رقم جديد للوحة
# ==================================

def add_number():

    # قائمة المربعات الفاضية
    empty = []

    # فحص كل المربعات
    for r in range(4):
        for c in range(4):

            # إذا المربع فاضي نحفظ مكانه
            if board[r][c] == 0:
                empty.append((r, c))

    # إذا فيه مربع فاضي
    if empty:

        # اختيار مكان شبه عشوائي
        r, c = empty[random_number(len(empty))]

        # إضافة الرقم 2 أو 4
        board[r][c] = 4 if random_number(10) == 0 else 2


# ==================================
# 4. عرض لوحة اللعبة
# ==================================

def show_board():

    # عرض النقاط
    print("\nScore:", score)
    print("-" * 25)

    # عرض كل صف
    for row in board:

        # عرض كل رقم في الصف
        for number in row:

            # عرض نقطة إذا المربع فاضي
            if number == 0:
                print(f"{'.':^6}", end="")

            # عرض الرقم إذا المربع مستخدم
            else:
                print(f"{number:^6}", end="")

        # الانتقال لسطر جديد
        print()

    print("-" * 25)


# ==================================
# 5. دمج الأرقام المتشابهة
# ==================================

def merge(row):
    global score

    # حذف الأصفار من الصف مؤقتاً
    numbers = [n for n in row if n != 0]

    # قائمة لحفظ الأرقام بعد الدمج
    result = []

    # نبدأ من أول رقم
    i = 0

    while i < len(numbers):

        # إذا الرقم الحالي يساوي اللي بعده
        if i + 1 < len(numbers) and numbers[i] == numbers[i + 1]:

            # دمج الرقمين
            value = numbers[i] * 2

            # إضافة الرقم الجديد
            result.append(value)

            # زيادة نقاط اللاعب
            score += value

            # الانتقال بعد الرقمين المدموجين
            i += 2

        else:

            # إضافة الرقم بدون دمج
            result.append(numbers[i])
            i += 1

    # إضافة أصفار حتى يصير طول الصف 4
    while len(result) < 4:
        result.append(0)

    # إرجاع الصف الجديد
    return result


# ==================================
# 6. تحريك الأرقام
# ==================================

# W = فوق
# A = يسار
# S = تحت
# D = يمين

def move(direction):

    # معرفة إذا اللوحة تغيرت
    changed = False

    for i in range(4):

        # الحركة يمين أو يسار
        if direction in ["a", "d"]:
            positions = [(i, j) for j in range(4)]

        # الحركة فوق أو تحت
        else:
            positions = [(j, i) for j in range(4)]

        # عكس الترتيب لليمين أو تحت
        if direction in ["d", "s"]:
            positions.reverse()

        # حفظ الأرقام القديمة
        old = [board[r][c] for r, c in positions]

        # دمج الأرقام
        new = merge(old)

        # التحقق إذا صارت حركة
        if old != new:
            changed = True

        # تحديث لوحة اللعبة
        for j in range(4):
            r, c = positions[j]
            board[r][c] = new[j]

    return changed


# ==================================
# 7. التأكد من خسارة اللاعب
# ==================================

def game_over():

    # فحص كل مربع
    for r in range(4):
        for c in range(4):

            # إذا فيه مربع فاضي، اللعبة مستمرة
            if board[r][c] == 0:
                return False

            # إذا فيه رقم مشابه تحته
            if r < 3 and board[r][c] == board[r + 1][c]:
                return False

            # إذا فيه رقم مشابه على اليمين
            if c < 3 and board[r][c] == board[r][c + 1]:
                return False

    # لا توجد حركة ممكنة
    return True


# ==================================
# 8. حفظ اللعبة في ملف JSON
# ==================================

# هذي أهم إضافة في Exercise 07
# نحفظ اللوحة والنقاط و seed
# بدون استخدام أي مكتبات

def save_game():

    # فتح ملف JSON للكتابة
    with open("save.json", "w") as file:

        # بداية JSON
        file.write("{\n")

        # حفظ نقاط اللاعب
        file.write('  "score": ' + str(score) + ',\n')

        # حفظ قيمة seed
        file.write('  "seed": ' + str(seed) + ',\n')

        # بداية قائمة اللوحة
        file.write('  "board": [\n')

        # حفظ الصفوف الأربعة
        for i in range(4):

            # تحويل الأرقام إلى نصوص
            numbers = [str(n) for n in board[i]]

            # جمع الأرقام بفواصل
            file.write("    [" + ", ".join(numbers) + "]")

            # إضافة فاصلة إلا بعد آخر صف
            if i < 3:
                file.write(",")

            # الانتقال لسطر جديد
            file.write("\n")

        # إغلاق قائمة اللوحة
        file.write("  ]\n")

        # إغلاق ملف JSON
        file.write("}\n")


# ==================================
# 9. تحميل اللعبة المحفوظة
# ==================================

# قراءة ملف JSON السابق
# وإرجاع اللوحة والنقاط كما كانت

def load_game():
    global board, score, seed

    try:

        # فتح ملف الحفظ للقراءة
        with open("save.json", "r") as file:
            lines = file.readlines()

        # قراءة النقاط من السطر الثاني
        new_score = int(lines[1].split(":")[1].strip().rstrip(","))

        # قراءة seed من السطر الثالث
        new_seed = int(lines[2].split(":")[1].strip().rstrip(","))

        # قائمة لتخزين اللوحة المحفوظة
        new_board = []

        # قراءة الصفوف الأربعة من JSON
        for i in range(4):

            # إزالة الأقواس والفواصل الخارجية
            row = lines[i + 4].strip().strip("[],")

            # تحويل النص إلى أرقام
            numbers = [int(n.strip()) for n in row.split(",")]

            # إضافة الصف للقائمة
            new_board.append(numbers)

        # التأكد أن حجم اللوحة صحيح
        if len(new_board) != 4:
            return False

        for row in new_board:
            if len(row) != 4:
                return False

            for number in row:
                if number < 0 or (number != 0 and
                    (number & (number - 1)) != 0):
                    return False

        # التأكد أن النقاط وقيمة seed صحيحتان
        if new_score < 0 or not 0 <= new_seed < 2147483648:
            return False

        # استرجاع البيانات القديمة
        board = new_board
        score = new_score
        seed = new_seed

        return True

    # إذا الملف غير موجود أو بياناته غير صحيحة
    except (FileNotFoundError, ValueError, IndexError, OSError):
        return False


# ==================================
# 10. القائمة الرئيسية للعبة
# ==================================

print("===== 2048 GAME =====")
print("1. New Game")
print("2. Continue Game")

# طلب اختيار المستخدم
choice = input("Choose 1 or 2: ")

# إذا اختار استكمال اللعبة
if choice == "2":

    # محاولة تحميل اللعبة
    if load_game():
        print("Saved game loaded!")

    else:
        # إذا ما فيه ملف حفظ صالح
        print("No valid saved game found!")
        print("Starting new game.")

        # بدء لعبة جديدة
        add_number()
        add_number()

        # حفظ اللعبة الجديدة
        save_game()

else:

    # بدء لعبة جديدة
    add_number()
    add_number()

    # حفظ اللعبة الجديدة
    save_game()


# ==================================
# 11. تشغيل اللعبة
# ==================================

while True:

    # عرض اللوحة والنقاط
    show_board()

    # التحقق من الفوز
    if any(2048 in row for row in board):
        print("You Win!")
        break

    # التحقق من الخسارة
    if game_over():
        print("Game Over!")
        break

    # طلب حركة من اللاعب
    direction = input(
        "Move W/A/S/D, P to save, Q to quit: "
    ).lower()

    # ==================================
    # 12. حفظ اللعبة والخروج
    # ==================================

    # إذا اختار Q نحفظ اللعبة ونخرج
    if direction == "q":

        save_game()

        print("Game saved successfully!")
        print("Goodbye!")
        break

    # إذا اختار P نحفظ ونكمل
    if direction == "p":

        save_game()

        print("Game saved successfully!")
        continue

    # التأكد أن الحركة صحيحة
    if direction not in ["w", "a", "s", "d"]:
        print("Invalid choice!")
        continue

    # تحريك الأرقام
    if move(direction):

        # إضافة رقم جديد بعد الحركة
        add_number()

        # حفظ اللعبة تلقائياً بعد كل حركة
        save_game()

    else:
        print("No movement possible!")
