import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def main():
    try:
        db_url = os.environ.get("DATABASE_URL")
        if not db_url:
            print("Ошибка: Переменная DATABASE_URL не найдена в файле .env")
            return
            
        conn = psycopg2.connect(db_url)
        cursor = conn.cursor()
    except Exception as e:
        print(f"Ошибка подключения к базе данных: {e}")
        return

    try:
        sql_query = input("Введите SQL-запрос:\n")
    except (KeyboardInterrupt, EOFError):
        print("\nПрограмма завершена.")
        cursor.close()
        conn.close()
        return

    sql_upper = sql_query.upper().strip()

    if not sql_upper.startswith("SELECT"):
        print("Ошибка: разрешены только SELECT-запросы")
        cursor.close()
        conn.close()
        return

    if "LIMIT" not in sql_upper:
        if sql_query.endswith(";"):
            sql_query = sql_query[:-1]
        sql_query += " LIMIT 5"

    try:
        cursor.execute(sql_query)
        records = cursor.fetchall()
        
        if records:
            colnames = [desc[0] for desc in cursor.description]
            print("\n" + " | ".join(colnames))
            print("-" * 60)
            for row in records:
                print(" | ".join(str(item) for item in row))
            print("-" * 60)
        else:
            print("Запрос выполнен успешно, но данных для отображения нет.")

    except Exception as e:
        print(f"Ошибка при выполнении запроса: {e}")
    
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    main()
