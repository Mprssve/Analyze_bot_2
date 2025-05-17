import mysql.connector

def get_error_tips(errors):
    conn = mysql.connector.connect(
        host="ВАШ_HOST",
        user="ВАШ_USER",
        password="ВАШ_PASSWORD",
        database="./iphone_panic_dump.db"
    )
    cursor = conn.cursor(dictionary=True)
    tips = []
    for error in errors:
        cursor.execute("SELECT tip FROM error_tips WHERE error_code=%s", (error,))
        row = cursor.fetchone()
        if row:
            tips.append(row["tip"])
    cursor.close()
    conn.close()
    return tips
