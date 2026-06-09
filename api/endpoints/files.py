from fastapi import APIRouter, Depends, HTTPException
from db import get_db
from models.files import FileCreate
import psycopg2.extras
import logging
import json

router = APIRouter()
logger = logging.getLogger("uvicorn.error")

## GET files
@router.get("/files")
def get_files(cur = Depends(get_db)):
    cur.execute("""
        SELECT *
        FROM files
        ORDER BY created_at DESC
    """)

    return cur.fetch_all()

## POST files
@router.post("/files")
def add_files(files: FileCreate, cur = Depends(get_db)):
    logger.info(f"METHOD: POST /files")
    logger.info(f"PAYLOAD: {files.model_dump()}")
    cur.execute("""
        SELECT 
            re.id AS run_experiment_id
        FROM experiments e
        JOIN samples s ON e.sample_id = s.id
        JOIN run_experiments re ON re.experiment_id = e.id
        JOIN sequencing_runs sq ON re.run_id = sq.id
        WHERE s.sample_name = %s
        AND e.assay_type = %s
        AND e.library_prep_date = %s
        AND sq.flowcell_id = %s
    """, (
        files.sample_name,
        files.assay_type,
        files.library_prep_date,
        files.flowcell_id
    ))

    result = cur.fetchone()

    if not result:
        logger.error("NO MATCH FOUND FOR INPUT:")
        logger.error({
            "sample_name": files.sample_name,
            "assay_type": files.assay_type,
            "library_prep_date": files.library_prep_date,
            "flowcell_id": files.flowcell_id
        })

        raise HTTPException(
            status_code=400,
            detail="No matching experiment/run combination found"
        )

    run_experiment_id = result["run_experiment_id"]

    #Table insertion
    cur.execute("""
        INSERT INTO files(
            run_experiment_id, gcs_uri, gcs_bucket, file_path, file_type, file_format, size_bytes, checksum_md5, extra_metadata
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING id
    """, (run_experiment_id, files.gcs_uri, files.gcs_bucket, files.file_path, files.file_type, files.file_format, 
          files.size_bytes ,files.checksum_md5, psycopg2.extras.Json(files.extra_metadata)))

    file_id = cur.fetchone()["id"]

    return {
        "id" : file_id
    }


## PATCH files

@router.patch("/files/{file_id}")
def update_files(file_id: str, payload: dict, cur = Depends(get_db)):
    IMMUTABLE = ["id", "created_at", "updated_at"]
    payload = {k: v for k, v in payload.items() if k not in IMMUTABLE}

    if not payload:
        raise HTTPException(400, "No valid fields to update")

    # If run_experiment natural keys were provided in future, resolve here (none currently)

    if "extra_metadata" in payload and payload["extra_metadata"] is not None:
        payload["extra_metadata"] = json.dumps(payload["extra_metadata"])

    fields = list(payload.keys())
    values = list(payload.values())
    set_clause = ", ".join([f"{k} = %s" for k in fields])

    query = f"""
        UPDATE files
        SET {set_clause}, updated_at = CURRENT_TIMESTAMP
        WHERE id = %s
        RETURNING *
    """

    cur.execute(query, (*values, file_id))
    result = cur.fetchone()

    if not result:
        raise HTTPException(404, "File not found")

    return result