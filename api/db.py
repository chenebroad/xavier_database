import psycopg2
import psycopg2.extras
import os
from typing import Generator

def get_conn():
    return psycopg2.connect(
        host=f"/cloudsql/{os.environ['CLOUDSQL_INSTANCE']}",
        dbname=os.environ["DB_NAME"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        port=5432
    )

def get_db() -> Generator:
    conn = get_conn()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    try:
        yield cur
        conn.commit()
    finally:
        cur.close()
        conn.close()