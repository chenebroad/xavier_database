from fastapi import APIRouter, Depends, HTTPException
from typing import Optional
from db import get_db
from models import MetadataRegistryCreate

router = APIRouter()

METADATA_ENTITIES = {
    "projects", "subjects", "samples", "cohorts", "experiments",
    "pools", "sequencing_runs", "flowcell_libraries", "files",
}


@router.get("/metadata_registry")
def list_registry(entity_type: Optional[str] = None, cur=Depends(get_db)):
    if entity_type:
        cur.execute("""
            SELECT * FROM metadata_registry
            WHERE entity_type = %s AND deprecated = false
            ORDER BY entity_type, field_name
        """, (entity_type,))
    else:
        cur.execute("""
            SELECT * FROM metadata_registry
            WHERE deprecated = false
            ORDER BY entity_type, field_name
        """)
    return cur.fetchall()


@router.post("/metadata_registry")
def add_registry_entry(entry: MetadataRegistryCreate, cur=Depends(get_db)):
    if entry.entity_type not in METADATA_ENTITIES:
        raise HTTPException(400,
            f"entity_type must be one of: {sorted(METADATA_ENTITIES)}"
        )
    if entry.data_type == "enum" and not entry.allowed_values:
        raise HTTPException(400, "allowed_values is required when data_type is 'enum'")

    cur.execute("""
        SELECT 1 FROM metadata_registry
        WHERE entity_type = %s AND field_name = %s AND deprecated = false
    """, (entry.entity_type, entry.field_name))
    if cur.fetchone():
        raise HTTPException(409,
            f"Field '{entry.field_name}' is already registered for '{entry.entity_type}'"
        )

    cur.execute("""
        INSERT INTO metadata_registry
            (entity_type, field_name, data_type, required, allowed_values, description)
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING *
    """, (
        entry.entity_type, entry.field_name, entry.data_type,
        entry.required, entry.allowed_values, entry.description,
    ))
    return cur.fetchone()


@router.patch("/metadata_registry/{registry_id}")
def update_registry_entry(registry_id: int, payload: dict, cur=Depends(get_db)):
    EDITABLE = {"description", "deprecated", "allowed_values"}
    payload = {k: v for k, v in payload.items() if k in EDITABLE}
    if not payload:
        raise HTTPException(400, f"Editable fields: {sorted(EDITABLE)}")

    fields = list(payload.keys())
    values = list(payload.values())
    set_clause = ", ".join(f"{k} = %s" for k in fields)

    cur.execute(f"""
        UPDATE metadata_registry SET {set_clause}
        WHERE id = %s RETURNING *
    """, (*values, registry_id))

    result = cur.fetchone()
    if not result:
        raise HTTPException(404, "Registry entry not found")
    return result
