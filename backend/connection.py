import os, psycopg2 ## This is the tool to execute the database in the python 
from dotenv import load_dotenv
load_dotenv()

connection = psycopg2.connect(os.environ["DATABASE_URL"])
cursor = connection.cursor()
cursor.execute("SELECT COUNT(*) FROM chunks")
print(cursor.fetchone())