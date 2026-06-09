from fastapi import APIRouter, Depends, HTTPException
from db import get_db
from models.experiments import ExperimentCreate
import psycopg2.extras
import json

router = APIRouter()

## GET experiments

@router.get("/experiments")
def get_experiments(cur = Depends(get_db)):

    cur.execute("""
        SELECT *
        FROM experiments
        ORDER BY created_at DESC
    """)

    return cur.fetchall()

## PATCH experiments

@router.patch("/experiments/{experiment_id}")
def update_experiment(experiment_id: str, payload: dict, cur = Depends(get_db)):
    IMMUTABLE = ["id", "created_at", "updated_at"]

    payload = {k: v for k, v in payload.items() if k not in IMMUTABLE}

    if not payload:
        raise HTTPException(400, "No valid fields to update")

    # Resolve natural key: sample_name -> sample_id
    if "sample_name" in payload:
        cur.execute("SELECT id FROM samples WHERE sample_name = %s", (payload["sample_name"],))
        result = cur.fetchone()
        if not result:
            raise HTTPException(400, f"sample_name '{payload['sample_name']}' does not exist")

        payload["sample_id"] = result["id"]
        del payload["sample_name"]

    # Serialize extra_metadata if present
    if "extra_metadata" in payload and payload["extra_metadata"] is not None:
        payload["extra_metadata"] = json.dumps(payload["extra_metadata"])

    # Build SQL
    fields = list(payload.keys())
    values = list(payload.values())
    set_clause = ", ".join([f"{k} = %s" for k in fields])

    query = f"""
        UPDATE experiments
        SET {set_clause}, updated_at = CURRENT_TIMESTAMP
        WHERE id = %s
        RETURNING *
    """

    cur.execute(query, (*values, experiment_id))
    result = cur.fetchone()

    if not result:
        raise HTTPException(404, "Experiment not found")

    return result

## POST samples

@router.post("/experiments")
def add_experiment(experiment: ExperimentCreate, cur=Depends(get_db)):
    # Lookup sample_id by natural key
    cur.execute("SELECT id FROM samples WHERE sample_name = %s", (experiment.sample_name,))
    sample_row = cur.fetchone()
    if not sample_row:
        raise HTTPException(status_code=404, detail=f"Sample '{experiment.sample_name}' not found")
    sample_id = sample_row["id"]

    cur.execute("""
        INSERT INTO experiments (
            sample_id, assay_type, library_protocol, library_prep_date, 
            library_version, extra_metadata
        )
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING id
    """, (
        sample_id, experiment.assay_type, experiment.library_protocol, experiment.library_prep_date,
        experiment.library_version, psycopg2.extras.Json(experiment.extra_metadata)
    ))

    experiment_id = cur.fetchone()["id"]
    return {"id": experiment_id, "assay_type": experiment.assay_type, "library_protocol": experiment.library_protocol}