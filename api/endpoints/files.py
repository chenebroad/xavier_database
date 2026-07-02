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
def get_files(cur=Depends(get_db)):
    cur.execute("""
        SELECT *
        FROM files
        ORDER BY created_at DESC
    """)
    return cur.fetchall()

## POST files
@router.post("/files")
def add_files(files: FileCreate, cur=Depends(get_db)):
    logger.info(f"METHOD: POST /files")
    logger.info(f"PAYLOAD: {files.model_dump()}")

    # Resolve natural keys to flowcell_library_id
    cur.execute("""
        SELECT fl.id AS flowcell_library_id
        FROM flowcell_libraries fl
        JOIN experiments e      ON fl.experiment_id = e.id
        JOIN samples s          ON e.sample_id = s.id
        JOIN sequencing_runs sq ON fl.run_id = sq.id
        WHERE s.sample_name       = %s
          AND e.assay_type        = %s
          AND e.library_prep_date = %s
          AND sq.flowcell_id      = %s
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
            "sample_name":       files.sample_name,
            "assay_type":        files.assay_type,
            "library_prep_date": files.library_prep_date,
            "flowcell_id":       files.flowcell_id
        })
        raise HTTPException(400, "No matching flowcell library found for the given sample/assay/date/flowcell")

    flowcell_library_id = result["flowcell_library_id"]

    cur.execute("""
        INSERT INTO files (
            flowcell_library_id, subject_id,
            gcs_uri, gcs_bucket, file_path,
            file_type, file_format,
            extra_metadata
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING id
    """, (
        flowcell_library_id, files.subject_id,
        files.gcs_uri, files.gcs_bucket, files.file_path,
        files.file_type, files.file_format,
        psycopg2.extras.Json(files.extra_metadata)
    ))

    return {"id": cur.fetchone()["id"]}

## PATCH files
@router.patch("/files/{file_id}")
def update_files(file_id: str, payload: dict, cur=Depends(get_db)):
    IMMUTABLE = ["id", "flowcell_library_id", "created_at", "updated_at"]
    payload = {k: v for k, v in payload.items() if k not in IMMUTABLE}

    if not payload:
        raise HTTPException(400, "No valid fields to update")

    if "extra_metadata" in payload and payload["extra_metadata"] is not None:
        payload["extra_metadata"] = json.dumps(payload["extra_metadata"])

    fields = list(payload.keys())
    values = list(payload.values())
    set_clause = ", ".join([f"{k} = %s" for k in fields])

    cur.execute(f"""
        UPDATE files
        SET {set_clause}, updated_at = CURRENT_TIMESTAMP
        WHERE id = %s
        RETURNING *
    """, (*values, file_id))

    result = cur.fetchone()
    if not result:
        raise HTTPException(404, "File not found")
    return result

## DELETE files
@router.delete("/files/{file_id}")
def delete_file(file_id: str, cur=Depends(get_db)):
    try:
        cur.execute("""
            DELETE FROM files
            WHERE id = %s
            RETURNING *
        """, (file_id,))
        result = cur.fetchone()
        if not result:
            raise HTTPException(404, "File not found")
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))
