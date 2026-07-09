from fastapi import APIRouter, Depends, HTTPException
from db import get_db
from models import PoolMembersCreate
import psycopg2.extras
import json

router = APIRouter()

@router.get("/pool_members")
def get_pool_members(cur=Depends(get_db)):
    cur.execute("""
        SELECT
            pm.pool_id,
            p.pool_name,
            pm.experiment_id,
            s.sample_name,
            e.assay_type,
            e.library_prep_date,
            pm.created_at
        FROM pool_members pm
        JOIN pools p       ON pm.pool_id = p.id
        JOIN experiments e ON pm.experiment_id = e.id
        JOIN samples s     ON e.sample_id = s.id
        ORDER BY pm.added_at DESC
    """)
    return cur.fetchall()


@router.post("/pool_members")
def add_pool_member(member: PoolMembersCreate, cur=Depends(get_db)):
    # Resolve pool_name → pool_id
    cur.execute("""
        SELECT id FROM pools WHERE pool_name = %s
    """, (member.pool_name,))
    pool = cur.fetchone()
    if not pool:
        raise HTTPException(404, f"Pool '{member.pool_name}' not found")

    # Resolve sample_name + assay_type + library_prep_date → experiment_id
    cur.execute("""
        SELECT e.id
        FROM experiments e
        JOIN samples s ON e.sample_id = s.id
        WHERE s.sample_name = %s
          AND e.assay_type = %s
          AND e.library_prep_date = %s
    """, (member.sample_name, member.assay_type, member.library_prep_date))
    experiment = cur.fetchone()
    if not experiment:
        raise HTTPException(404,
            f"No experiment found for sample '{member.sample_name}', "
            f"assay '{member.assay_type}', date '{member.library_prep_date}'"
        )

    # Guard against duplicate membership
    cur.execute("""
        SELECT 1 FROM pool_members
        WHERE pool_id = %s AND experiment_id = %s
    """, (pool["id"], experiment["id"]))
    if cur.fetchone():
        raise HTTPException(409,
            f"Experiment for '{member.sample_name}' / '{member.assay_type}' / "
            f"'{member.library_prep_date}' is already in pool '{member.pool_name}'"
        )

    cur.execute("""
        INSERT INTO pool_members (pool_id, experiment_id)
        VALUES (%s, %s)
        RETURNING *
    """, (pool["id"], experiment["id"]))

    return cur.fetchone()


@router.delete("/pool_members")
def remove_pool_member(
    pool_name: str,
    sample_name: str,
    assay_type: str,
    library_prep_date: str,
    cur=Depends(get_db)
):
    cur.execute("""
        DELETE FROM pool_members
        WHERE pool_id = (
            SELECT id FROM pools WHERE pool_name = %s
        )
        AND experiment_id = (
            SELECT e.id
            FROM experiments e
            JOIN samples s ON e.sample_id = s.id
            WHERE s.sample_name = %s
              AND e.assay_type = %s
              AND e.library_prep_date = %s
        )
        RETURNING *
    """, (pool_name, sample_name, assay_type, library_prep_date))

    if not cur.fetchone():
        raise HTTPException(404, "Membership not found")