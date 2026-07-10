from typing import Any, Dict
from db import get_conn
import psycopg2.extras


def get_metadata_registry(entity_type: str) -> Dict[str, dict]:
    """Fetch registry entries for entity_type. No cache — always reflects current state."""
    conn = get_conn()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("""
        SELECT field_name, data_type, allowed_values
        FROM metadata_registry
        WHERE entity_type = %s AND deprecated = false
    """, (entity_type,))
    rows = cur.fetchall()
    cur.close()
    conn.close()

    return {
        r["field_name"]: {
            "data_type":      r["data_type"],
            "allowed_values": r["allowed_values"] or None,  # TEXT[] arrives as a list
        }
        for r in rows
    }


def validate_extra_metadata(entity_type: str, extra_metadata: Dict[str, Any]) -> None:
    """
    Soft-validates extra_metadata keys against the registry.
    Unknown keys pass through — the registry is advisory, not exhaustive.
    Known keys are type- and value-checked when the registry entry specifies constraints.
    """
    if not extra_metadata:
        return

    registry = get_metadata_registry(entity_type)

    type_map = {
        "str": str, "text": str,
        "int": int, "integer": int,
        "float": float,
        "bool": bool, "boolean": bool,
    }

    for field, value in extra_metadata.items():
        if field not in registry:
            continue

        meta = registry[field]

        py_type = type_map.get(meta.get("data_type"))
        if py_type and not isinstance(value, py_type):
            raise ValueError(
                f"extra_metadata field '{field}' must be type "
                f"{meta['data_type']}, got {type(value).__name__}"
            )

        allowed = meta.get("allowed_values")
        if allowed and str(value) not in allowed:
            raise ValueError(
                f"extra_metadata field '{field}' must be one of {allowed}, got '{value}'"
            )
