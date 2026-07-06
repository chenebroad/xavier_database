from fastapi import APIRouter, Depends, HTTPException
from db import get_db

router = APIRouter()

@router.get("/query")
def query_table(table: str, limit: int = 100, cur=Depends(get_db)):
    allowed_tables = [
        "projects",
        "samples",
        "subjects",
        "sample_sources",
        "cohorts",
        "cohort_members",
        "experiments",
        "pools",
        "pool_members",
        "sequencing_runs",
        "flowcell_libraries",
        "files",
    ]

    if table not in allowed_tables:
        raise HTTPException(status_code=400, detail=f"Invalid table '{table}'")

    match table:
        case "projects":
            query = "SELECT * FROM projects ORDER BY created_at DESC LIMIT %s"
        case "samples":
            query = """
                SELECT s.*, p.project_name
                FROM samples s
                LEFT JOIN projects p ON s.project_id = p.id
                ORDER BY s.created_at DESC
                LIMIT %s"""
        case "subjects":
            query = "SELECT * FROM subjects ORDER BY added_at DESC LIMIT %s"
        case "sample_sources":
            query = """
                SELECT ss.*, s.sample_name, su.pub_id, su.freezerworks_id
                FROM sample_sources ss
                JOIN samples s  ON ss.sample_id  = s.id
                JOIN subjects su ON ss.subject_id = su.id
                ORDER BY ss.added_at DESC
                LIMIT %s"""
        case "cohorts":
            query = "SELECT * FROM cohorts ORDER BY created_at DESC LIMIT %s"
        case "cohort_members":
            query = """
                SELECT cm.*, c.cohort_name, s.sample_name
                FROM cohort_members cm
                JOIN cohorts c ON cm.cohort_id = c.id
                JOIN samples s ON cm.sample_id = s.id
                ORDER BY cm.added_at DESC
                LIMIT %s"""
        case "experiments":
            query = """
                SELECT e.*, s.sample_name
                FROM experiments e
                LEFT JOIN samples s ON e.sample_id = s.id
                ORDER BY e.created_at DESC
                LIMIT %s"""
        case "pools":
            query = "SELECT * FROM pools ORDER BY created_at DESC LIMIT %s"
        case "pool_members":
            query = """
                SELECT pm.*, p.pool_name, s.sample_name, e.assay_type, e.library_prep_date
                FROM pool_members pm
                JOIN pools p       ON pm.pool_id       = p.id
                JOIN experiments e ON pm.experiment_id = e.id
                JOIN samples s     ON e.sample_id      = s.id
                ORDER BY pm.added_at DESC
                LIMIT %s"""
        case "sequencing_runs":
            query = "SELECT * FROM sequencing_runs ORDER BY created_at DESC LIMIT %s"
        case "flowcell_libraries":
            query = """
                SELECT fl.*, s.sample_name, e.assay_type, e.library_prep_date, sq.flowcell_id
                FROM flowcell_libraries fl
                LEFT JOIN experiments e    ON fl.experiment_id = e.id
                LEFT JOIN samples s        ON e.sample_id      = s.id
                LEFT JOIN sequencing_runs sq ON fl.run_id      = sq.id
                ORDER BY fl.created_at DESC
                LIMIT %s"""
        case "files":
            query = """
                SELECT f.*, s.sample_name, e.assay_type, e.library_prep_date, sq.flowcell_id
                FROM files f
                LEFT JOIN flowcell_libraries fl ON f.flowcell_library_id = fl.id
                LEFT JOIN experiments e         ON fl.experiment_id = e.id
                LEFT JOIN samples s             ON e.sample_id      = s.id
                LEFT JOIN sequencing_runs sq    ON fl.run_id        = sq.id
                ORDER BY f.created_at DESC
                LIMIT %s"""

    cur.execute(query, (limit,))
    return cur.fetchall()
