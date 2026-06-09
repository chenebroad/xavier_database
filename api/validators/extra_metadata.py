from typing import Dict, Any
from db import get_conn
import psycopg2.extras
from functools import lru_cache

@lru_cache(maxsize=10)
def get_metadata_registry(entity_type: str) -> Dict[str, dict]:
    conn = get_conn()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    cur.execute("""
        SELECT field_name, data_type, allowed_values
        FROM metadata_registry
        WHERE entity_type = %s
    """, (entity_type,))
    rows = cur.fetchall()
    cur.close()
    conn.close()

    registry = {}
    for r in rows:
        registry[r["field_name"]] = {
            "data_type": r["data_type"],
            "allowed_values": r["allowed_values"].split(",") if r["allowed_values"] else None
        }
    return registry

def validate_extra_metadata(entity_type: str, extra_metadata: Dict[str, Any]) -> None:
    registry = get_metadata_registry(entity_type)

    type_map = {
        "str": str,
        "int": int,
        "float": float,
        "bool": bool
    }

    for field, value in extra_metadata.items():
        if field not in registry:
            continue  # allow extra fields not in registry
        meta = registry[field]

        # check type
        expected_type = meta.get("data_type")
        py_type = type_map.get(expected_type)
        if py_type and not isinstance(value, py_type):
            raise ValueError(
                f"Field '{field}' must be of type {expected_type}, got {type(value).__name__}"
            )

        # check allowed values
        allowed = meta.get("allowed_values")
        if allowed and str(value) not in allowed:
            raise ValueError(
                f"Field '{field}' must be one of {allowed}, got '{value}'"
            )