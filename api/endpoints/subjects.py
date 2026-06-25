from fastapi import APIRouter, Depends, HTTPException
from db import get_db
from models.subjects import SubjectCreate
import psycopg2.extras
import json

router = APIRouter()

@router.get("/subjects")
def get_subjects(cur=Depends(get_db)):
    cur.execute("""
        SELECT *
        FROM subjects 
        ORDER BY created_at DESC
    """)
    return cur.fetchall()

@router.post("/subjects")
def add_subject(subject: SubjectCreate, cur=Depends(get_db)):
    # Guard against duplicate pub_id + freezerworks_id combination
    cur.execute("""
        SELECT 1 FROM subjects
        WHERE pub_id = %s AND freezerworks_id = %s
    """, (subject.pub_id, subject.freezerworks_id))
    if cur.fetchone():
        raise HTTPException(409,
            f"Subject with pub_id '{subject.pub_id}' and "
            f"freezerworks_id '{subject.freezerworks_id}' already exists"
        )

    cur.execute("""
        INSERT INTO subjects (pub_id, freezerworks_id, extra_metadata)
        VALUES (%s, %s, %s)
        RETURNING *
    """, (
        subject.pub_id,
        subject.freezerworks_id,
        psycopg2.extras.Json(subject.extra_metadata or {})
    ))
    return cur.fetchone()


@router.patch("/subjects/{pub_id}")
def update_subject(pub_id: str, payload: dict, cur=Depends(get_db)):
    IMMUTABLE = ["id", "created_at", "updated_at"]

    payload = {k: v for k, v in payload.items() if k not in IMMUTABLE}

    if not payload:
        raise HTTPException(400, "No valid fields to update")

    if "extra_metadata" in payload and payload["extra_metadata"] is not None:
        payload["extra_metadata"] = json.dumps(payload["extra_metadata"])

    fields     = list(payload.keys())
    values     = list(payload.values())
    set_clause = ", ".join([f"{k} = %s" for k in fields])

    cur.execute(f"""
        UPDATE subjects
        SET {set_clause}
        WHERE pub_id = %s
        RETURNING *
    """, (*values, pub_id))

    result = cur.fetchone()
    if not result:
        raise HTTPException(404, f"Subject with pub_id '{pub_id}' not found")
    return result