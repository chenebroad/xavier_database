from fastapi import APIRouter, Depends, HTTPException
from db import get_db
from models.sample_sources import SampleSourceCreate

router = APIRouter()

@router.get("/sample_sources")
def get_sample_sources(cur=Depends(get_db)):
    cur.execute("""
        SELECT *
        FROM sample_sources ss
        ORDER BY ss.added_at DESC
    """)
    return cur.fetchall()


@router.post("/sample_sources")
def add_sample_source(source: SampleSourceCreate, cur=Depends(get_db)):
    # Resolve sample_name → sample_id
    cur.execute("""
        SELECT id FROM samples WHERE sample_name = %s
    """, (source.sample_name,))
    sample = cur.fetchone()
    if not sample:
        raise HTTPException(404, f"Sample '{source.sample_name}' not found")

    # Resolve subject_pub_id → subject_id
    cur.execute("""
        SELECT id FROM subjects WHERE pub_id = %s AND freezerworks_id = %s
    """, (source.pub_id, source.freezerworks_id))
    subject = cur.fetchone()
    if not subject:
        raise HTTPException(404, f"Subject with pub_id '{source.subject_pub_id}' not found")

    # Guard against duplicate
    cur.execute("""
        SELECT 1 FROM sample_sources
        WHERE sample_id = %s AND subject_id = %s
    """, (sample["id"], subject["id"]))
    if cur.fetchone():
        raise HTTPException(409,
            f"Subject '{source.subject_pub_id}' is already "
            f"linked to sample '{source.sample_name}'"
        )

    cur.execute("""
        INSERT INTO sample_sources (sample_id, subject_id)
        VALUES (%s, %s)
        RETURNING *
    """, (sample["id"], subject["id"]))

    return cur.fetchone()


@router.delete("/sample_sources")
def remove_sample_source(sample_name: str, subject_pub_id: str, cur=Depends(get_db)):
    cur.execute("""
        DELETE FROM sample_sources
        WHERE sample_id = (
            SELECT id FROM samples WHERE sample_name = %s
        )
        AND subject_id = (
            SELECT id FROM subjects WHERE pub_id = %s
        )
        RETURNING *
    """, (sample_name, subject_pub_id))

    if not cur.fetchone():
        raise HTTPException(404, "Sample source link not found")