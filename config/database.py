import psycopg2
from psycopg2.extras import RealDictCursor
import time

max_retries = 5  # Limit to 5 retries
retries = 0

while retries < max_retries:
    try:
        connect = psycopg2.connect(
            host='localhost',
            database='fastapi',
            user='postgres',
            password='12ab34sd01@',
            cursor_factory=RealDictCursor
        )
        cursor = connect.cursor()
        print('Database connection is successful')
        break  # Exit the loop if connection is successful
    except Exception as error:
        print('Connection failed')
        print(error)
        retries += 1
        time.sleep(2)

if retries == max_retries:
    print("Max retries reached. Could not connect to the database.")
