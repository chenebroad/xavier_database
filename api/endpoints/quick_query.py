from fastapi import APIRouter, Depends, HTTPException
from typing import Optional
from db import get_db

router = APIRouter()

@router.get("/quick_query")
def quick_query(
    query_type: str,
    project_name: Optional[str] = None,
    sample_name:  Optional[str] = None,
    cohort_name:  Optional[str] = None,
    pool_name:    Optional[str] = None,
    cur=Depends(get_db)
):
    def require(param, name):
        if not param:
            raise HTTPException(400, f"{name} is required for this query type")

    try:
        match query_type:

            case "samples_by_project":
                require(project_name, "project_name")
                cur.execute("""
                    SELECT
                        s.*,
                        p.project_name
                    FROM samples s
                    JOIN projects p ON s.project_id = p.id
                    WHERE p.project_name = %s
                """, (project_name,))

            case "experiments_by_sample":
                require(sample_name, "sample_name")
                cur.execute("""
                    SELECT
                        e.*,
                        s.sample_name
                    FROM experiments e
                    JOIN samples s ON e.sample_id = s.id
                    WHERE s.sample_name = %s
                """, (sample_name,))

            case "files_by_sample":
                require(sample_name, "sample_name")
                cur.execute("""
                    SELECT
                        f.*,
                        e.assay_type,
                        s.sample_name,
                        sq.flowcell_id
                    FROM files f
                    JOIN flowcell_libraries fl ON f.flowcell_library_id = fl.id
                    JOIN experiments e         ON fl.experiment_id = e.id
                    JOIN sequencing_runs sq    ON fl.run_id = sq.id
                    JOIN samples s             ON e.sample_id = s.id
                    WHERE s.sample_name = %s
                """, (sample_name,))

            case "files_by_project":
                require(project_name, "project_name")
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
                    JOIN flowcell_libraries fl ON f.flowcell_library_id = fl.id
                    JOIN experiments e         ON fl.experiment_id = e.id
                    JOIN sequencing_runs sq    ON fl.run_id = sq.id
                    JOIN samples s             ON e.sample_id = s.id
                    JOIN projects p            ON s.project_id = p.id
                    WHERE p.project_name = %s
                """, (project_name,))

            case "samples_by_cohort":
                require(cohort_name, "cohort_name")
                cur.execute("""
                    SELECT
                        s.*,
                        c.cohort_name,
                        c.cohort_type
                    FROM samples s
                    JOIN cohort_members cm ON s.id = cm.sample_id
                    JOIN cohorts c         ON cm.cohort_id = c.id
                    WHERE c.cohort_name = %s
                    ORDER BY s.sample_name
                """, (cohort_name,))

            case "subjects_by_sample":
                require(sample_name, "sample_name")
                cur.execute("""
                    SELECT
                        su.id             AS subject_id,
                        su.pub_id,
                        su.freezerworks_id,
                        s.sample_name,
                        s.sample_type
                    FROM subjects su
                    JOIN sample_sources ss ON su.id = ss.subject_id
                    JOIN samples s         ON ss.sample_id = s.id
                    WHERE s.sample_name = %s
                    ORDER BY su.pub_id
                """, (sample_name,))

            case "experiments_by_pool":
                require(pool_name, "pool_name")
                cur.execute("""
                    SELECT
                        e.*,
                        s.sample_name,
                        p.pool_name
                    FROM experiments e
                    JOIN pool_members pm ON e.id = pm.experiment_id
                    JOIN pools p         ON pm.pool_id = p.id
                    JOIN samples s       ON e.sample_id = s.id
                    WHERE p.pool_name = %s
                    ORDER BY s.sample_name, e.assay_type
                """, (pool_name,))

            case _:
                raise HTTPException(400, f"Unknown query_type '{query_type}'")

        return cur.fetchall()

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))