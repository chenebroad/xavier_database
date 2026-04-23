from fastapi import APIRouter, Depends, Query, HTTPException
from typing import Optional, List
from ..db import get_db

router = APIRouter()

@router.get("/query")
def query_table(table: str, limit: int = 100, cur=Depends(get_db)):
    allowed_tables = [
        "projects",
        "samples",
        "experiments",
        "sequencing_runs",
        "run_experiments",
        "files"
    ]

    if table not in allowed_tables:
        raise HTTPException(status_code=400, detail="Invalid table")

    match table:
        case "projects":
            query = "SELECT * FROM projects"
        case "samples":
            query = """SELECT
                        s.*,
                        p.project_name
                    FROM samples s
                    LEFT JOIN projects p ON s.project_id = p.id
                    ORDER BY s.created_at DESC
                    LIMIT %s"""
        case "experiments":
            query = """SELECT
                        e.*,
                        s.sample_name
                    FROM experiments e
                    LEFT JOIN samples s ON e.sample_id = s.id
                    ORDER BY s.created_at DESC
                    LIMIT %s"""
        case "sequencing_runs":
            query = "SELECT * FROM sequencing_runs"
        case "run_experiments":
            query = """SELECT
                        re.*,
                        s.sample_name,
                        e.assay_type,
                        e.library_prep_date,
                        r.flowcell_id
                    FROM run_experiments re
                    LEFT JOIN experiments e ON re.experiment_id = e.id
                    LEFT JOIN samples s ON e.sample_id = s.id
                    LEFT JOIN sequencing_runs r ON re.run_id = r.id
                    ORDER BY re.created_at DESC
                    LIMIT %s"""
        case "files":
            query = """SELECT
                        f.*,
                        s.sample_name,
                        e.assay_type,
                        e.library_prep_date,
                        r.flowcell_id
                    FROM files f
                    LEFT JOIN run_experiments re ON f.run_experiment_id = re.id
                    LEFT JOIN experiments e ON re.experiment_id = e.id
                    LEFT JOIN samples s ON e.sample_id = s.id
                    LEFT JOIN sequencing_runs r ON re.run_id = r.id
                    ORDER BY f.created_at DESC
                    LIMIT %s"""

    cur.execute(query, (limit,))
    results = cur.fetchall()

    return results

# # Map user-facing fields → actual SQL columns
# ALLOWED_FIELDS = {
#     "sample_name": "s.sample_name",
#     "assay_type": "e.assay_type",
#     "library_prep_date": "e.library_prep_date",
#     "flowcell_id": "r.flowcell_id",
#     "experiment_run_id": "re.id",
#     "file_id": "f.id",
#     "file_path": "f.file_path",
#     "file_type": "f.file_type",
#     "extra_metadata": "f.extra_metadata"
# }


# @router.get("/query")
# def query_data(
#     sample_name: Optional[str] = None,
#     assay_type: Optional[str] = None,
#     flowcell_id: Optional[str] = None,
#     file_type: Optional[str] = None,

#     # NEW: advanced filters
#     advanced: Optional[List[str]] = Query(None),

#     fields: Optional[str] = Query(None),
#     include_metadata: bool = False,

#     metadata_key: Optional[str] = None,
#     metadata_value: Optional[str] = None,

#     cur=Depends(get_db)
# ):
#     # -----------------------------
#     # 1️⃣ Build SELECT clause
#     # -----------------------------
#     if fields:
#         requested_fields = [f.strip() for f in fields.split(",")]

#         # Validate fields
#         invalid = [f for f in requested_fields if f not in ALLOWED_FIELDS]
#         if invalid:
#             return {"error": f"Invalid fields requested: {invalid}"}

#         select_clause = ", ".join(
#             f"{ALLOWED_FIELDS[f]} AS {f}" for f in requested_fields
#         )
#     else:
#         # Default fields (safe + useful)
#         base_fields = [
#             "sample_name",
#             "assay_type",
#             "flowcell_id",
#             "file_path",
#             "file_type"
#         ]

#         if include_metadata:
#             base_fields.append("extra_metadata")

#         select_clause = ", ".join(
#             f"{ALLOWED_FIELDS[f]} AS {f}" for f in base_fields
#         )

#     # -----------------------------
#     # 2️⃣ Base query (JOIN chain)
#     # -----------------------------
#     query = f"""
#         SELECT {select_clause}
#         FROM samples s
#         JOIN experiments e ON s.sample_name = e.sample_name
#         JOIN run_experiments re ON e.id = re.experiment_id
#         JOIN sequencing_runs r ON re.run_id = r.id
#         LEFT JOIN files f ON f.experiment_run_id = re.id
#     """

#     params = []

#     # -----------------------------
#     # 3️⃣ Core filters
#     # -----------------------------
#     if sample_name:
#         query += " AND s.sample_name = %s"
#         params.append(sample_name)

#     if assay_type:
#         query += " AND e.assay_type = %s"
#         params.append(assay_type)

#     if flowcell_id:
#         query += " AND r.flowcell_id = %s"
#         params.append(flowcell_id)

#     if file_type:
#         query += " AND f.file_type = %s"
#         params.append(file_type)

#     # -----------------------------
#     # 4️⃣ Advanced filters
#     # -----------------------------
#     if advanced:
#         for f in advanced:
#             try:
#                 # format: table.column=value
#                 left, value = f.split("=", 1)
#                 table, column = left.split(".", 1)

#                 table_map = {
#                     "samples": "s",
#                     "experiments": "e",
#                     "sequencing_runs": "r",
#                     "files": "f"
#                 }

#                 if table not in table_map:
#                     return {"error": f"Invalid table: {table}"}

#                 alias = table_map[table]

#                 query += f" AND {alias}.{column} = %s"
#                 params.append(value)

#             except Exception:
#                 return {"error": f"Invalid advanced filter format: {f}"}
#     # -----------------------------
#     # 5 Metadata filter (JSONB)
#     # -----------------------------
#     if metadata_key and metadata_value:
#         query += " AND f.extra_metadata ->> %s = %s"
#         params.extend([metadata_key, metadata_value])

#     # -----------------------------
#     # 6 Execute query
#     # -----------------------------
#     cur.execute(query, params)
#     rows = cur.fetchall()

#     # -----------------------------
#     # 6️⃣ Convert to JSON
#     # -----------------------------
#     results = []
#     for row in rows:
#         results.append(dict(row))

#     return results