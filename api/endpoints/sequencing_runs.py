from fastapi import APIRouter, Depends, HTTPException
from db import get_db
from models import SequencingCreate
import psycopg2.extras
import json

router = APIRouter()

## GET sequencing

@router.get("/sequencing")
def get_sequencing(cur= Depends(get_db)):

    cur.execute("""
        SELECT *
        FROM sequencing_runs
        ORDER BY created_at DESC
    """)

    return cur.fetchall()

## POST sequencing

@router.post("/sequencing")
def add_sequencing(sequencing: SequencingCreate, cur = Depends(get_db)):
    cur.execute("""
        INSERT INTO sequencing_runs (
            flowcell_id, machine, run_date, read_length, sequencing_center, bcl_gcs_uri, extra_metadata
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        RETURNING id
    """, (
        sequencing.flowcell_id, sequencing.machine, sequencing.run_date, sequencing.read_length,
        sequencing.sequencing_center, sequencing.bcl_gcs_uri, psycopg2.extras.Json(sequencing.extra_metadata)
    ))
    
    sequencing_id = cur.fetchone()["id"]
    return {
        "id": sequencing_id
    }


## PATCH sequencing

@router.patch("/sequencing/{sequencing_id}")
def update_sequencing(sequencing_id: str, payload: dict, cur = Depends(get_db)):
    IMMUTABLE = ["id", "created_at", "updated_at"]
    payload = {k: v for k, v in payload.items() if k not in IMMUTABLE}

    if not payload:
        raise HTTPException(400, "No valid fields to update")

    if "extra_metadata" in payload and payload["extra_metadata"] is not None:
        payload["extra_metadata"] = json.dumps(payload["extra_metadata"])

    fields = list(payload.keys())
    values = list(payload.values())
    set_clause = ", ".join([f"{k} = %s" for k in fields])

    query = f"""
        UPDATE sequencing_runs
        SET {set_clause}, updated_at = CURRENT_TIMESTAMP
        WHERE id = %s
        RETURNING *
    """

    cur.execute(query, (*values, sequencing_id))
    result = cur.fetchone()

    if not result:
        raise HTTPException(404, "Sequencing run not found")

    return result

## DELETE sequencing
@router.delete("/sequencing/{sequencing_id}")
def delete_sequencing(sequencing_id: str, cur=Depends(get_db)):
    try:
        cur.execute("""
            DELETE FROM sequencing_runs
            WHERE id = %s
            RETURNING *
        """, (sequencing_id,))
        result = cur.fetchone()
        if not result:
            raise HTTPException(404, "Sequencing run not found")
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))