import re
from fastapi import APIRouter, Depends, HTTPException
from db import get_db

router = APIRouter()

_BLOCKED = re.compile(
    r'\b(INSERT|UPDATE|DELETE|DROP|CREATE|ALTER|TRUNCATE|GRANT|REVOKE|EXECUTE|EXEC|COPY)\b',
    re.IGNORECASE,
)


@router.post("/sql")
def run_custom_sql(body: dict, cur=Depends(get_db)):
    sql = (body.get("sql") or "").strip()
    if not sql:
        raise HTTPException(400, "No SQL provided")
    if not re.match(r'^\s*SELECT\b', sql, re.IGNORECASE):
        raise HTTPException(400, "Only SELECT statements are permitted")
    if _BLOCKED.search(sql):
        raise HTTPException(400, "Query contains a disallowed keyword")
    try:
        cur.execute(sql)
        return cur.fetchall()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(400, str(e))
