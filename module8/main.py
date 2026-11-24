# نستدعي مكتبة FastMCP
from fastmcp import FastMCP

# نستدعي مكتبة التاريخ
from datetime import datetime

# نستدعي مكتبة الأرقام العشوائية
import random

# ننشئ سيرفر MCP
mcp = FastMCP("My MCP Server")

# ننشئ أداة لعرض تاريخ النظام
@mcp.tool()
def get_date():
    return datetime.now().strftime("%Y-%m-%d")

# ننشئ أداة لإرجاع رقم عشوائي
@mcp.tool()
def get_random_number():
    return random.randint(1, 100)

# نشغل سيرفر MCP
if __name__ == "__main__":
    mcp.run()