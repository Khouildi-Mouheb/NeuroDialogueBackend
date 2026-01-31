from django.test import TestCase
import psycopg2
import os
from dotenv import load_dotenv

conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password=os.getenv("PASSWORD_SUPABASE"),
    host="db.soucjbozdevdhieqflhp.supabase.co",
    port=5432
)
print("Connected to Supabase!")
conn.close()
