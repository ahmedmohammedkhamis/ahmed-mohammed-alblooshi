# نستدعي مكتبة MCP
from fastmcp import FastMCP

# نستدعي مكتبة قاعدة البيانات
import sqlite3

# نستدعي مكتبة لتحديد مكان الملف
from pathlib import Path

# ننشئ سيرفر MCP
mcp = FastMCP("Database MCP")

# نحدد مكان قاعدة البيانات
db = Path(__file__).with_name("ahmed_module8_2.db")

# ننشئ أداة لاستخراج بيانات المستخدمين
@mcp.tool()
def get_users():

    # نتصل بقاعدة البيانات
    conn = sqlite3.connect(db)

    # ننشئ أداة لتنفيذ أوامر SQL
    cursor = conn.cursor()

    # نستخرج جميع المستخدمين
    cursor.execute("SELECT * FROM users")

    # نحفظ النتائج في متغير
    users = cursor.fetchall()

    # نغلق الاتصال بقاعدة البيانات
    conn.close()

    # نرجع النتائج إلى MCP Inspector
    return users

# نشغل سيرفر MCP
if __name__ == "__main__":
    mcp.run()