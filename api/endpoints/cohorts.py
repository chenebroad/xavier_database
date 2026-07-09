from fastapi import APIRouter, Depends, HTTPException
from db import get_db
from models import CohortCreate
import psycopg2.extras
import json

router = APIRouter()

## GET cohorts

@router.get("/cohorts")
def get_cohorts(cur = Depends(get_db)):
    
    cur.execute("""
        SELECT *
        FROM cohorts
        ORDER BY created_at DESC
    """)

    return cur.fetchall()

## PATCH cohorts
@router.patch("/cohorts/{cohort_id}")
def update_cohort(cohort_id: str, payload: dict, cur = Depends(get_db)):
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
        UPDATE cohorts
        SET {set_clause}, updated_at = CURRENT_TIMESTAMP
        WHERE id = %s
        RETURNING *
    """, (*values, cohort_id))

    result = cur.fetchone()
    if not result:
        raise HTTPException(404, f"Cohort {cohort_id} not found")
    return result

## POST cohorts
@router.post("/cohorts")
def add_cohort(cohort: CohortCreate, cur = Depends(get_db)):
    cur.execute("""
        INSERT INTO cohorts (cohort_name, cohort_type, description, extra_metadata)
        VALUES (%s, %s, %s, %s)
        RETURNING *
    """, (
        cohort.cohort_name,
        cohort.cohort_type,
        cohort.description,
        psycopg2.extras.Json(cohort.extra_metadata or {})
    ))

    return cur.fetchone()

## DELETE cohorts
@router.delete("/cohorts/{cohort_id}")
def delete_cohort(cohort_id: str, cur=Depends(get_db)):
    try:
        cur.execute("""
            DELETE FROM cohorts
            WHERE id = %s
            RETURNING *
        """, (cohort_id,))
        result = cur.fetchone()
        if not result:
            raise HTTPException(404, "Cohort not found")
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))