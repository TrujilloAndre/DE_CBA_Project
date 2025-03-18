import mysql.connector
from dotenv import load_dotenv
import os

dotenv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../Storage.env'))
load_dotenv(dotenv_path)

conn = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    passwd=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)
cursor = conn.cursor()

cursor.execute("ALTER TABLE sales MODIFY id INT AUTO_INCREMENT PRIMARY KEY")
cursor.execute("ALTER TABLE sales MODIFY store_id VARCHAR(200) NOT NULL")
cursor.execute("ALTER TABLE sales MODIFY total_sales DECIMAL(10,2) NOT NULL")
cursor.execute("ALTER TABLE sales MODIFY date DATE NOT NULL")

conn.commit()
cursor.close()
conn.close()


print("Data type altered successfully")