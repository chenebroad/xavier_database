from fastapi import APIRouter, Depends, HTTPException
from ..db import get_db
from ..models.projects import ProjectCreate
import psycopg2.extras
import json

router = APIRouter()

## GET projects

@router.get("/projects")
def get_projects(cur = Depends(get_db)):
    cur.execute("""
        SELECT *
        FROM projects
        ORDER BY created_at DESC
    """)

    return cur.fetchall()

## PATCH projects
@router.patch("/projects/{project_id}")
def update_project(project_id: str, payload: dict, cur = Depends(get_db)):

    IMMUTABLE = ["id", "created_at", "updated_at"]
    payload = {k: v for k, v in payload.items() if k not in IMMUTABLE}

    if not payload:
        raise HTTPException(400, "No valid fields to update")

    if "extra_metadata" in payload and payload["extra_metadata"] is not None:
        payload["extra_metadata"] = json.dumps(payload["extra_metadata"])

    set_clause = ", ".join([f"{k} = %s" for k in payload.keys()])
    values = list(payload.values())

    query = f"""
        UPDATE projects
        SET {set_clause}, updated_at = CURRENT_TIMESTAMP
        WHERE id = %s
        RETURNING *
    """

    cur.execute(query, (*values, project_id))
    result = cur.fetchone()

    if not result:
        raise HTTPException(404, "Sample not found")

    return result  
## POST projects

@router.post("/projects")
def add_project(project: ProjectCreate, cur = Depends(get_db)):
    cur.execute("""
        INSERT INTO projects (project_name, description, extra_metadata)
        VALUES (%s, %s, %s)         
        RETURNING id
    """, (project.project_name, project.description, psycopg2.extras.Json(project.extra_metadata)))

    project_id = cur.fetchone()["id"]

    return {
        "id": project_id,
        "project_name": project.project_name
    }