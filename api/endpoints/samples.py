from fastapi import APIRouter, Depends, HTTPException
from ..db import get_db
from ..models.samples import SampleCreate
import psycopg2.extras
import json

router = APIRouter()

## GET samples

@router.get("/samples")
def get_samples(cur = Depends(get_db)):
    cur.execute("""
        SELECT *
        FROM samples
        ORDER BY created_at DESC            
    """)

    return cur.fetchall()

## PATCH samples

@router.patch("/samples/{sample_id}")
def update_samples(sample_id: str, payload: dict, cur = Depends(get_db)):
    
    IMMUTABLE = ["id", "created_at", "updated_at"]

    payload = {k: v for k, v in payload.items() if k not in IMMUTABLE}

    if not payload:
        raise HTTPException(400, "No valid fields to update")


    # -------------------------
    # Resolve natural keys FIRST
    # -------------------------
    if "project_name" in payload:
        cur.execute("""
            SELECT id FROM projects WHERE project_name = %s
        """, (payload["project_name"],))

        result = cur.fetchone()
        if not result:
            raise HTTPException(400, f"project_name '{payload['project_name']}' does not exist")

        payload["project_id"] = result["id"]
        del payload["project_name"]


    # -------------------------
    # Serialize special fields
    # -------------------------
    if "extra_metadata" in payload and payload["extra_metadata"] is not None:
        payload["extra_metadata"] = json.dumps(payload["extra_metadata"])


    # -------------------------
    # Build SQL AFTER all mutations
    # -------------------------
    fields = list(payload.keys())
    values = list(payload.values())

    set_clause = ", ".join([f"{k} = %s" for k in fields])


    # -------------------------
    # Execute single update
    # -------------------------
    query = f"""
        UPDATE samples
        SET {set_clause}, updated_at = CURRENT_TIMESTAMP
        WHERE id = %s
        RETURNING *
    """

    cur.execute(query, (*values, sample_id))

    result = cur.fetchone()

    if not result:
        raise HTTPException(404, "Sample not found")

    return result

## POST samples

@router.post("/samples")
def add_sample(sample: SampleCreate, cur=Depends(get_db)):
    # Lookup project_id by natural key
    cur.execute("SELECT id FROM projects WHERE project_name = %s", (sample.project_name,))
    project_row = cur.fetchone()
    if not project_row:
        raise HTTPException(status_code=404, detail=f"Project '{sample.project_name}' not found")
    project_id = project_row["id"]

    cur.execute("""
        INSERT INTO samples (
            project_id, sample_name, subject_id, status, organism, tissue, extra_metadata
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        RETURNING id
    """, (
        project_id, sample.sample_name, sample.subject_id, sample.status,
        sample.organism, sample.tissue, psycopg2.extras.Json(sample.extra_metadata)
    ))

    sample_id = cur.fetchone()["id"]
    return {"id": sample_id, "sample_name": sample.sample_name, "sample_status": sample.status}