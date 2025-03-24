import psycopg2
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Creat function to connect to PostgreSQL database using database credentials from .env
def connect_db():
    return psycopg2.connect(
        dbname=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT'),
    )