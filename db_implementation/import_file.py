import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

dotenv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../Storage.env'))
load_dotenv(dotenv_path)

cba_file = os.getenv("CBA_FILE_PATH")

df = pd.read_csv(cba_file, dtype=str)
df = df.rename(columns={"store_code":"store_id", "total_sale":"total_sales","transaction_date": "date"})
df['total_sales'] = df['total_sales'].str.replace('$', '')
df['total_sales'] = df['total_sales'].str.replace(',', '')
df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')

engine = create_engine(os.getenv('SQLALCHEMY_DATABASE_URI'))

df.to_sql('sales', con=engine, if_exists='replace', index=False)

print("Data Imported Successfully")