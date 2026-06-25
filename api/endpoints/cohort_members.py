from fastapi import APIRouter, Depends, HTTPException
from db import get_db
from models.cohort_members import CohortMembersCreate
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

## POST cohort_members
@router.post("/cohort_members")
def add_cohort_member(member: CohortMembersCreate, cur = Depends(get_db)):
    # Resolve cohort_name → cohort_id
    cur.execute("SELECT id FROM cohorts WHERE cohort_name = %s", (member.cohort_name,))
    cohort = cur.fetchone()
    if not cohort:
        raise HTTPException(404, f"Cohort '{member.cohort_name}' not found")

    # Resolve sample_name → sample_id
    cur.execute("SELECT id FROM samples WHERE sample_name = %s", (member.sample_name,))
    sample = cur.fetchone()
    if not sample:
        raise HTTPException(404, f"Sample '{member.sample_name}' not found")

    # Guard against duplicate membership
    cur.execute("""
        SELECT 1 FROM cohort_members
        WHERE cohort_id = %s AND sample_id = %s
    """, (cohort["id"], sample["id"]))
    if cur.fetchone():
        raise HTTPException(409, f"Sample '{member.sample_name}' is already in cohort '{member.cohort_name}'")

    cur.execute("""
        INSERT INTO cohort_members (cohort_id, sample_id)
        VALUES (%s, %s)
        RETURNING *
    """, (cohort["id"], sample["id"]))

    return cur.fetchone()

@router.delete("/cohort_members")
def remove_cohort_member(cohort_name: str, sample_name: str, cur=Depends(get_db)):
    cur.execute("""
        DELETE FROM cohort_members
        WHERE cohort_id = (SELECT id FROM cohorts WHERE cohort_name = %s)
        AND sample_id = (SELECT id FROM samples WHERE sample_name = %s)
        RETURNING *
    """, (cohort_name, sample_name))

    if not cur.fetchone():
        raise HTTPException(404, "Membership not found")