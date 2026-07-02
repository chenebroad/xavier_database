from fastapi import APIRouter, Depends, HTTPException
from db import get_db
from models.flowcell_libraries import SeqExpCreate
import psycopg2.extras
import json

router = APIRouter()

## GET flowcell_libraries
@router.get("/flowcell_libraries")
def get_flowcell_libraries(cur=Depends(get_db)):
    cur.execute("""
        SELECT
            fl.id,
            fl.lane,
            fl.index_sequence,
            fl.extra_metadata,
            fl.created_at,
            fl.updated_at,
            s.sample_name,
            e.assay_type,
            e.library_prep_date,
            sq.flowcell_id
        FROM flowcell_libraries fl
        JOIN experiments e        ON fl.experiment_id = e.id
        JOIN samples s            ON e.sample_id = s.id
        JOIN sequencing_runs sq   ON fl.run_id = sq.id
        ORDER BY fl.created_at DESC
    """)
    return cur.fetchall()

## POST flowcell_libraries
@router.post("/flowcell_libraries")
def add_flowcell_library(seq_exp: SeqExpCreate, cur=Depends(get_db)):
    # Resolve experiment natural key
    cur.execute("""
        SELECT e.id
        FROM experiments e
        JOIN samples s ON e.sample_id = s.id
        WHERE s.sample_name = %s
          AND e.assay_type = %s
          AND e.library_prep_date = %s
    """, (seq_exp.sample_name, seq_exp.assay_type, seq_exp.library_prep_date))

    row = cur.fetchone()
    if not row:
        raise HTTPException(404,
            f"Experiment not found for sample '{seq_exp.sample_name}', "
            f"assay '{seq_exp.assay_type}', date '{seq_exp.library_prep_date}'"
        )
    experiment_id = row["id"]

    # Resolve flowcell natural key
    cur.execute("""
        SELECT id FROM sequencing_runs WHERE flowcell_id = %s
    """, (seq_exp.flowcell_id,))

    row = cur.fetchone()
    if not row:
        raise HTTPException(404, f"Sequencing run '{seq_exp.flowcell_id}' not found")
    run_id = row["id"]

    # Guard duplicate
    cur.execute("""
        SELECT 1 FROM flowcell_libraries
        WHERE experiment_id = %s AND run_id = %s AND lane = %s
    """, (experiment_id, run_id, seq_exp.lane))
    if cur.fetchone():
        raise HTTPException(409,
            f"Library already assigned to flowcell '{seq_exp.flowcell_id}' lane '{seq_exp.lane}'"
        )

    cur.execute("""
        INSERT INTO flowcell_libraries (experiment_id, run_id, lane, index_sequence, extra_metadata)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING *
    """, (experiment_id, run_id, seq_exp.lane, seq_exp.index_sequence,
          psycopg2.extras.Json(seq_exp.extra_metadata)))

    return cur.fetchone()

## PATCH flowcell_libraries
@router.patch("/flowcell_libraries/{flowcell_library_id}")
def update_flowcell_library(flowcell_library_id: str, payload: dict, cur=Depends(get_db)):
    IMMUTABLE = ["id", "experiment_id", "run_id", "created_at", "updated_at"]
    payload = {k: v for k, v in payload.items() if k not in IMMUTABLE}

    if not payload:
        raise HTTPException(400, "No valid fields to update")

    # Resolve experiment natural key if provided
    if all(k in payload for k in ("sample_name", "assay_type", "library_prep_date")):
        cur.execute("""
            SELECT e.id
            FROM experiments e
            JOIN samples s ON e.sample_id = s.id
            WHERE s.sample_name = %s AND e.assay_type = %s AND e.library_prep_date = %s
        """, (payload["sample_name"], payload["assay_type"], payload["library_prep_date"]))
        row = cur.fetchone()
        if not row:
            raise HTTPException(400, "Experiment natural key lookup failed")
        payload["experiment_id"] = row["id"]
        del payload["sample_name"], payload["assay_type"], payload["library_prep_date"]

    # Resolve flowcell natural key if provided
    if "flowcell_id" in payload:
        cur.execute("SELECT id FROM sequencing_runs WHERE flowcell_id = %s", (payload["flowcell_id"],))
        row = cur.fetchone()
        if not row:
            raise HTTPException(400, f"flowcell_id '{payload['flowcell_id']}' not found")
        payload["run_id"] = row["id"]
        del payload["flowcell_id"]

    if "extra_metadata" in payload and payload["extra_metadata"] is not None:
        payload["extra_metadata"] = json.dumps(payload["extra_metadata"])

    fields = list(payload.keys())
    values = list(payload.values())
    set_clause = ", ".join([f"{k} = %s" for k in fields])

    cur.execute(f"""
        UPDATE flowcell_libraries
        SET {set_clause}, updated_at = CURRENT_TIMESTAMP
        WHERE id = %s
        RETURNING *
    """, (*values, flowcell_library_id))

    result = cur.fetchone()
    if not result:
        raise HTTPException(404, "Flowcell library not found")
    return result

## DELETE flowcell_libraries
@router.delete("/flowcell_libraries/{flowcell_library_id}")
def delete_flowcell_library(flowcell_library_id: str, cur=Depends(get_db)):
    try:
        cur.execute("""
            DELETE FROM flowcell_libraries
            WHERE id = %s
            RETURNING *
        """, (flowcell_library_id,))
        result = cur.fetchone()
        if not result:
            raise HTTPException(404, "Flowcell library not found")
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))
