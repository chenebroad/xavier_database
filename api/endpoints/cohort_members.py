from fastapi import APIRouter, Depends, HTTPException
from db import get_db
from models.cohorts import CohortMembersCreate
import psycopg2.extras
import json

router = APIRouter()

## GET cohort_members
@router.get("/cohort_members")
def get_cohort_members(cur=Depends(get_db)):

    cur.execute("""
        SELECT *
        FROM cohort_members
        ORDER by created_at DESC
    """)
    
    return cur.fetchall()

## PATCH cohort_members
@router.patch("/cohort_members/{member_id}")
def update_cohort_member(member_id: str, payload: dict, cur = Depends(get_db)):
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
        UPDATE cohort_members
        SET {set_clause}, updated_at = CURRENT_TIMESTAMP
        WHERE id = %s
        RETURNING *
    """

    cur.execute(query, (*values, member_id))
    result = cur.fetchone()

## POST cohort_members
def add_cohort_member(member: CohortMembersCreate, cur = Depends(get_db)):
    cur.execute("""
        INSERT INTO cohort_members (cohort_id, member_id, member_type, extra_metadata)
        VALUES (%s, %s, %s, %s)
        RETURNING *
    """, (
        member.cohort_id,
        member.member_id,
        member.member_type,
        json.dumps(member.extra_metadata) if member.extra_metadata else None
    ))

    return cur.fetchone()