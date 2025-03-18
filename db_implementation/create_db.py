import mysql.connector
from dotenv import load_dotenv
import os

dotenv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../Storage.env'))
load_dotenv(dotenv_path)

conn = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    passwd=os.getenv("DB_PASSWORD")
)

my_cursor = conn.cursor()

my_cursor.execute("CREATE DATABASE IF NOT EXISTS Store_Data")

my_cursor.execute("SHOW DATABASES")
for db in my_cursor:
    print(db)
