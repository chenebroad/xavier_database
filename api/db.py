import psycopg2
import psycopg2.extras
from .config import DB_CONFIG
from typing import Generator

def get_conn():
    return psycopg2.connect(**DB_CONFIG)

def get_db() -> Generator:
    conn = get_conn()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    try:
        yield cur
        conn.commit()
    finally:
        cur.close()
        conn.close()