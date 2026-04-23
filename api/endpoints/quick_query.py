from fastapi import APIRouter, Depends, Query, HTTPException
from typing import Optional, List
from ..db import get_db

router = APIRouter()

@router.get("/quick_query")
def quick_query(
    query_type: str,
    project_name: Optional[str] = None,
    sample_name: Optional[str] = None,
    cur=Depends(get_db)
):
    try:
        if query_type == "samples_by_project":
            if not project_name:
                raise HTTPException(status_code=400, detail="project_name required")

            cur.execute("""
                SELECT s.*
                FROM samples s
                JOIN projects p ON s.project_id = p.id
                WHERE p.project_name = %s
            """, (project_name,))
            return cur.fetchall()

        elif query_type == "experiments_by_sample":
            if not sample_name:
                raise HTTPException(status_code=400, detail="sample_name required")

            cur.execute("""
                SELECT e.*
                FROM experiments e
                JOIN samples s ON e.sample_id = s.id
                WHERE s.sample_name = %s
            """, (sample_name,))
            return cur.fetchall()

        elif query_type == "files_by_sample":
            if not sample_name:
                raise HTTPException(status_code=400, detail="sample_name required")

            cur.execute("""
                SELECT f.*, e.assay_type, sq.flowcell_id
                FROM files f
                JOIN run_experiments re ON f.run_experiment_id = re.id
                JOIN experiments e ON re.experiment_id = e.id
                JOIN sequencing_runs sq ON re.run_id = sq.id
                JOIN samples s ON e.sample_id = s.id
                WHERE s.sample_name = %s
            """, (sample_name,))
            return cur.fetchall()

        elif query_type == "files_by_project":
            if not project_name:
                raise HTTPException(status_code=400, detail="project_name required")

            cur.execute("""
                SELECT 
                    f.file_path,
                    f.gcs_uri,
                    f.file_type,
                    f.file_format,
                    s.sample_name,
                    e.assay_type,
                    sq.flowcell_id
                FROM files f
                JOIN run_experiments re ON f.run_experiment_id = re.id
                JOIN experiments e ON re.experiment_id = e.id
                JOIN sequencing_runs sq ON re.run_id = sq.id
                JOIN samples s ON e.sample_id = s.id
                JOIN projects p ON s.project_id = p.id
                WHERE p.project_name = %s
            """, (project_name,))
            return cur.fetchall()

        else:
            raise HTTPException(status_code=400, detail="Invalid query_type")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))