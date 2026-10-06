import os, psycopg2 ## This is the tool to execute the database in the python 
from dotenv import load_dotenv
load_dotenv()

connection = psycopg2.connect(os.environ["DATABASE_URL"])
cursor = connection.cursor() ## Creating cursor to execute the command
cursor.execute("SELECT * FROM chunks") 
print(cursor.fetchone())