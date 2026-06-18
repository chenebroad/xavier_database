from fastapi import APIRouter, Depends, HTTPException
from db import get_db
from models.cohorts import CohortCreate
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
@router.patch("/cohorts/cohort_id")
def update_cohort(cohort_id: str, payload: dict, cur = Depends(get_db)):
    IMMUTABLE = ["id", "created_at", "updated_at"]

    payload = {k: v for k, v in payload.items() if k not in IMMUTABLE}

    if not payload:
        raise HTTPException(400, "No valid fields to update")

    # Serialize extra_metadata if present
    if "extra_metadata" in payload and payload["extra_metadata"] is not None:
        payload["extra_metadata"] = json.dumps(payload["extra_metadata"])

    # Build SQL
    fields = list(payload.keys())
    values = list(payload.values())
    set_clause = ", ".join([f"{k} = %s" for k in fields])

    query = f"""
        UPDATE cohorts
        SET {set_clause}, updated_at = CURRENT_TIMESTAMP
        WHERE id = %s
        RETURNING *
    """

    cur.execute(query, (*values, cohort_id))
    result = cur.fetchone()

## POST cohorts
def add_cohort(cohort: CohortCreate, cur = Depends(get_db)):
    cur.execute("""
        INSERT INTO cohorts (cohort_name, project_name, description, extra_metadata)
        VALUES (%s, %s, %s, %s)
        RETURNING *
    """, (
        cohort.cohort_name,
        cohort.project_name,
        cohort.description,
        psycopg2.extras.Json(cohort.extra_metadata) if cohort.extra_metadata is not None else None
    ))

    return cur.fetchone()