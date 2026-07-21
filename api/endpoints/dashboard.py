from fastapi import APIRouter, Depends, HTTPException
from db import get_db

router = APIRouter()

@router.get("/dashboard/projects")
def get_project_summary(cur=Depends(get_db)):
    cur.execute("""
        SELECT
            p.id                            AS project_id,
            p.project_name,
            p.description,
            p.created_at,
            COUNT(DISTINCT sa.id)           AS sample_count,
            COUNT(DISTINCT e.id)            AS experiment_count,
            COUNT(DISTINCT fl.id)           AS run_count,
            COUNT(DISTINCT f.id)            AS file_count,
            COUNT(DISTINCT ss.subject_id)   AS subject_count,
            COUNT(DISTINCT sa.id) FILTER (
                WHERE sa.sample_type = 'pooled'
            )                               AS pooled_sample_count,
            COUNT(DISTINCT sa.id) FILTER (
                WHERE sa.sample_type = 'individual'
            )                               AS individual_sample_count
        FROM projects p
        LEFT JOIN samples sa              ON p.id  = sa.project_id
        LEFT JOIN experiments e           ON sa.id = e.sample_id
        LEFT JOIN flowcell_libraries fl   ON e.id  = fl.experiment_id
        LEFT JOIN files f                 ON f.flowcell_library_id = fl.id
        LEFT JOIN sample_sources ss       ON sa.id = ss.sample_id
        GROUP BY p.id, p.project_name, p.description, p.created_at
        ORDER BY p.created_at DESC
    """)
    return cur.fetchall()


@router.get("/dashboard/projects/{project_name}")
def get_project_detail(project_name: str, cur=Depends(get_db)):
    cur.execute("SELECT id FROM projects WHERE project_name = %s", (project_name,))
    project = cur.fetchone()
    if not project:
        raise HTTPException(404, f"Project '{project_name}' not found")

    cur.execute("""
        SELECT
            sa.id                               AS sample_id,
            sa.sample_name,
            sa.sample_type,
            sa.organism,
            sa.tissue,
            sa.status,
            COUNT(DISTINCT ss.subject_id)       AS subject_count,
            COUNT(DISTINCT e.id)                AS experiment_count,
            COUNT(DISTINCT fl.id)               AS run_count,
            COUNT(DISTINCT f.id)                AS file_count,
            (COUNT(DISTINCT e.id)  > 0)         AS has_experiment,
            (COUNT(DISTINCT fl.id) > 0)         AS has_run,
            (COUNT(DISTINCT f.id)  > 0)         AS has_files,
            (COUNT(DISTINCT ss.subject_id) > 0) AS has_subjects,
            COALESCE(
                array_agg(DISTINCT e.assay_type)
                FILTER (WHERE e.assay_type IS NOT NULL),
                '{}'
            )                                   AS assay_types
        FROM samples sa
        LEFT JOIN sample_sources ss           ON sa.id = ss.sample_id
        LEFT JOIN experiments e               ON sa.id = e.sample_id
        LEFT JOIN flowcell_libraries fl       ON e.id  = fl.experiment_id
        LEFT JOIN files f                     ON f.flowcell_library_id = fl.id
        WHERE sa.project_id = %s
        GROUP BY sa.id, sa.sample_name, sa.sample_type, sa.organism, sa.tissue
        ORDER BY sa.sample_name
    """, (project["id"],))

    return cur.fetchall()


@router.get("/dashboard/projects/{project_name}/cohorts")
def get_project_cohorts(project_name: str, cur=Depends(get_db)):
    cur.execute("SELECT id FROM projects WHERE project_name = %s", (project_name,))
    project = cur.fetchone()
    if not project:
        raise HTTPException(404, f"Project '{project_name}' not found")

    cur.execute("""
        SELECT
            c.cohort_name,
            c.cohort_type,
            COUNT(DISTINCT cm.sample_id) AS member_count
        FROM cohorts c
        JOIN cohort_members cm ON c.id  = cm.cohort_id
        JOIN samples sa        ON cm.sample_id = sa.id
        WHERE sa.project_id = %s
        GROUP BY c.id, c.cohort_name, c.cohort_type
        ORDER BY c.cohort_name
    """, (project["id"],))

    return cur.fetchall()
