import sqlite3
import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

USE_SQLITE = os.getenv('USE_SQLITE', 'True').lower() in ('true', '1', 't')
SQLITE_DB_PATH = os.path.join(os.path.dirname(__file__), 'database.sqlite')

DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_USER = os.getenv('DB_USER', 'root')
DB_PASS = os.getenv('DB_PASS', '')
DB_NAME = os.getenv('DB_NAME', 'sinergia_agro')

def get_db_connection():
    if USE_SQLITE:
        conn = sqlite3.connect(SQLITE_DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn
    else:
        conn = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASS,
            database=DB_NAME,
            cursorclass=pymysql.cursors.DictCursor
        )
        return conn

def execute_query(query, params=(), fetch=True):
    conn = get_db_connection()
    try:
        if USE_SQLITE:
            cursor = conn.cursor()
            cursor.execute(query, params)
            if fetch:
                result = cursor.fetchall()
                return [dict(row) for row in result]
            else:
                conn.commit()
                return cursor.lastrowid
        else:
            # PyMySQL requires %s for placeholders instead of ?
            if params:
                query = query.replace('?', '%s')
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                if fetch:
                    return cursor.fetchall()
                else:
                    conn.commit()
                    return cursor.lastrowid
    finally:
        conn.close()

def execute_query_single(query, params=()):
    res = execute_query(query, params, fetch=True)
    if res:
        return res[0]
    return None
