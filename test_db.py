import psycopg2

conn = psycopg2.connect(
    database="courier_db",
    user="courier_user",
    password="courier123",
    host="localhost",
    port="5432"
)

print("Database Connected Successfully!")

conn.close()