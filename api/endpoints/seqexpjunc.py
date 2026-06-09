from fastapi import APIRouter, Depends, HTTPException
from db import get_db
from models.seqexpjunc import SeqExpCreate
import psycopg2.extras
import json

router = APIRouter()

## GET seqexp

@router.get("/seqexp")
def get_sequencing_exp(cur = Depends(get_db)):

    cur.execute("""
        SELECT *
        FROM run_experiments
        ORDER BY created_at DESC
    """)

    return cur.fetchall()

## POST seqexp
@router.post("/seqexp")
def add_sequencing_exp(seq_exp: SeqExpCreate, cur = Depends(get_db)):
    #Retrieve experiment_id
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
        raise HTTPException(
            status_code=404,
            detail=f"Experiment lookup failed: {seq_exp.sample_name}, {seq_exp.assay_type}, {seq_exp.library_prep_date}"
        )
    experiment_id = row["id"]

    #Retrieve run_id
    cur.execute("""
        SELECT id FROM sequencing_runs
        WHERE flowcell_id = %s
    """, (seq_exp.flowcell_id,))

    row = cur.fetchone()
    if not row:
        raise HTTPException(
            status_code=404,
            detail=f"Sequencing run lookup failed: {seq_exp.flowcell_id}"
        )
    run_id = row["id"]

    #Table insertion
    cur.execute("""
        INSERT INTO run_experiments (experiment_id, run_id, lane, index_sequence, extra_metadata)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING experiment_id, run_id
        """, (experiment_id, run_id, seq_exp.lane, seq_exp.index_sequence,
              psycopg2.extras.Json(seq_exp.extra_metadata)))

    return {
        "experiment_id": experiment_id,
        "run_id" : run_id
    }


## PATCH seqexp

@router.patch("/seqexp/{run_experiment_id}")
@router.patch("/run_experiments/{run_experiment_id}")
def update_seqexp(run_experiment_id: str, payload: dict, cur = Depends(get_db)):
    IMMUTABLE = ["id", "experiment_id", "run_id", "created_at", "updated_at"]

    # allow updating experiment_id/run_id only via natural keys below, so remove if passed as raw
    payload = {k: v for k, v in payload.items() if k not in IMMUTABLE}

    if not payload:
        raise HTTPException(400, "No valid fields to update")

    # Natural key resolutions
    # If sample_name/assay_type/library_prep_date provided, resolve to experiment_id
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
        # remove natural parts
        del payload["sample_name"]
        del payload["assay_type"]
        del payload["library_prep_date"]

    # If flowcell_id provided, resolve to run_id
    if "flowcell_id" in payload:
        cur.execute("SELECT id FROM sequencing_runs WHERE flowcell_id = %s", (payload["flowcell_id"],))
        row = cur.fetchone()
        if not row:
            raise HTTPException(400, f"flowcell_id '{payload['flowcell_id']}' does not exist")

        payload["run_id"] = row["id"]
        del payload["flowcell_id"]

    if "extra_metadata" in payload and payload["extra_metadata"] is not None:
        payload["extra_metadata"] = json.dumps(payload["extra_metadata"])

    fields = list(payload.keys())
    values = list(payload.values())
    set_clause = ", ".join([f"{k} = %s" for k in fields])

    query = f"""
        UPDATE run_experiments
        SET {set_clause}, updated_at = CURRENT_TIMESTAMP
        WHERE id = %s
        RETURNING *
    """

    cur.execute(query, (*values, run_experiment_id))
    result = cur.fetchone()

    if not result:
        raise HTTPException(404, "Run-Experiment mapping not found")

    return result