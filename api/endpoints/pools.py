from fastapi import APIRouter, Depends, HTTPException
from db import get_db
from models import PoolCreate
import psycopg2.extras
import json

router = APIRouter()

# ── Pools ─────────────────────────────────────────────────────────────────────

@router.get("/pools")
def get_pools(cur=Depends(get_db)):
    cur.execute("""
        SELECT *
        FROM pools
        ORDER BY created_at DESC
    """)
    return cur.fetchall()


@router.post("/pools")
def add_pool(pool: PoolCreate, cur=Depends(get_db)):
    cur.execute("""
        INSERT INTO pools (pool_name, extra_metadata)
        VALUES (%s, %s)
        RETURNING *
    """, (
        pool.pool_name,
        psycopg2.extras.Json(pool.extra_metadata or {})
    ))
    return cur.fetchone()


@router.patch("/pools/{pool_id}")
def update_pool(pool_id: str, payload: dict, cur=Depends(get_db)):
    IMMUTABLE = ["id", "created_at", "updated_at"]
    payload = {k: v for k, v in payload.items() if k not in IMMUTABLE}

    if not payload:
        raise HTTPException(400, "No valid fields to update")

    if "extra_metadata" in payload and payload["extra_metadata"] is not None:
        payload["extra_metadata"] = json.dumps(payload["extra_metadata"])

    fields = list(payload.keys())
    values = list(payload.values())
    set_clause = ", ".join([f"{k} = %s" for k in fields])

    cur.execute(f"""
        UPDATE pools
        SET {set_clause}, updated_at = CURRENT_TIMESTAMP
        WHERE id = %s
        RETURNING *
    """, (*values, pool_id))

    result = cur.fetchone()
    if not result:
        raise HTTPException(404, f"Pool '{pool_id}' not found")
    return result

## DELETE pools
@router.delete("/pools/{pool_id}")
def delete_pool(pool_id: str, cur=Depends(get_db)):
    try:
        cur.execute("""
            DELETE FROM pools
            WHERE id = %s
            RETURNING *
        """, (pool_id,))
        result = cur.fetchone()
        if not result:
            raise HTTPException(404, "Pool not found")
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))
