from database import Database

try:
    cursor = Database.get_cursor()
    cursor.execute("SELECT 1")
    cursor.fetchall()  # ✅ consume result
    print("DB connection OK")
except Exception as e:
    print("DB error:", e)
finally:
    Database.close()
