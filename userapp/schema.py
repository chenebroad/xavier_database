"""
Single source of truth for Xavier LIMS table definitions.

Used by:
  - userapp/pages/ingest_data.py  (required/optional/no_metadata)
  - userapp/generate_erd.py       (full schema → xavier_erd_panel.html)

Field classifications:
  required    — must be present on ingest
  optional    — named field, can be omitted, has DB default
  system      — auto-managed (id, FKs, timestamps) — never in ingest forms
  no_metadata — True on junction tables (no extra_metadata column)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
HOW TO ADD A NEW TABLE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. schema.py  (this file)
   Add an entry to ENTITY_SCHEMAS with all required keys:
     label, color, colorBg, desc, required, optional, system,
     relations, pos
   Add "no_metadata": True if it is a junction table.
   Add edges to the EDGES list at the bottom.

2. api/models/<table>.py
   Create a Pydantic model for the POST body.
   Use natural keys (e.g. sample_name) not internal IDs.
   Mark Optional fields with Optional[str] = None.
   Add an extra_metadata validator unless it is a junction table.

3. api/endpoints/<table>.py
   Implement GET, POST, PATCH, DELETE following the existing patterns:
     - GET: joined view returning human-readable names
     - POST: resolve natural keys → internal IDs, guard duplicates (409)
     - PATCH: filter IMMUTABLE fields, set updated_at
     - DELETE: hard delete, return deleted row
   Always re-raise HTTPException before the generic Exception handler.

4. api/app.py
   Import the new router and register it:
     from endpoints import <table>
     app.include_router(<table>.router, prefix="/api")

5. userapp/pages/ingest_data.py
   Add the api function to API_FN:
     "new_table": create_new_table,
   Add the corresponding import at the top:
     from api_client import ..., create_new_table

6. userapp/api_client.py
   Add create_new_table() and delete_new_table() functions.

7. userapp/pages/query_data.py
   Add an entry to TABLES:
     "new_table": {"editable": True}  # or False if junction
   If junction, users see a read-only caption instead of an editor.

8. generate_erd.py  (no edits needed)
   Run it to regenerate the ERD panel:
     cd userapp && python generate_erd.py

9. migrations/
   Write the CREATE TABLE SQL in a new migration file.
   Run it against Cloud SQL before deploying.

JUNCTION TABLE CHECKLIST (sample_sources, cohort_members, pool_members)
  - no_metadata: True in schema.py
  - No extra_metadata column in SQL
  - No PATCH endpoint — only GET, POST, DELETE
  - Use composite PK (no surrogate id column)
  - Use added_at instead of created_at/updated_at
  - editable: False in query_data.py TABLES dict
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

ENTITY_SCHEMAS = {

    "projects": {
        "label":    "Projects",
        "color":    "#4f9cf9",
        "colorBg":  "#0d1f3c",
        "desc":     "Top-level scientific project or study.",
        "required": ["project_name"],
        "optional": ["description"],
        "system":   ["id", "created_at", "updated_at", "extra_metadata"],
        "relations": ["samples"],
        "pos":      {"x": 40, "y": 60},
    },

    "subjects": {
        "label":    "Subjects",
        "color":    "#a78bfa",
        "colorBg":  "#1a1435",
        "desc":     "A patient or donor contributing biological material.",
        "required": ["pub_id", "freezerworks_id"],
        "optional": [],
        "system":   ["id", "added_at", "extra_metadata"],
        "relations": ["sample_sources"],
        "pos":      {"x": 330, "y": 60},
    },

    "samples": {
        "label":    "Samples",
        "color":    "#2dd4bf",
        "colorBg":  "#0a2028",
        "desc":     "A biological specimen. Subject linkage is via sample_sources.",
        "required": ["sample_name", "project_name", "organism", "tissue"],
        "optional": ["sample_type"],
        "system":   ["id", "project_id", "created_at", "updated_at", "extra_metadata"],
        "relations": ["projects", "sample_sources", "experiments", "cohort_members"],
        "pos":      {"x": 185, "y": 185},
    },

    "sample_sources": {
        "label":       "Sample sources",
        "color":       "#a78bfa",
        "colorBg":     "#110e2a",
        "desc":        "Junction. Links subjects to samples. Pooled samples have one row per contributing subject.",
        "required":    ["sample_name", "pub_id", "freezerworks_id"],
        "optional":    [],
        "system":      ["sample_id", "subject_id", "added_at"],
        "relations":   ["samples", "subjects"],
        "pos":         {"x": 330, "y": 305},
        "no_metadata": True,
    },

    "cohorts": {
        "label":    "Cohorts",
        "color":    "#fbbf24",
        "colorBg":  "#241a04",
        "desc":     "A named grouping of biological samples — biological, technical, or analysis-defined.",
        "required": ["cohort_name"],
        "optional": ["cohort_type", "description"],
        "system":   ["id", "created_at", "updated_at", "extra_metadata"],
        "relations": ["cohort_members"],
        "pos":      {"x": 510, "y": 185},
    },

    "cohort_members": {
        "label":       "Cohort members",
        "color":       "#fbbf24",
        "colorBg":     "#1c1504",
        "desc":        "Junction. Links samples to cohorts. Many-to-many.",
        "required":    ["cohort_name", "sample_name"],
        "optional":    [],
        "system":      ["cohort_id", "sample_id", "added_at"],
        "relations":   ["cohorts", "samples"],
        "pos":         {"x": 510, "y": 305},
        "no_metadata": True,
    },

    "experiments": {
        "label":    "Experiments",
        "color":    "#4ade80",
        "colorBg":  "#0a1f10",
        "desc":     "A library preparation or assay performed on a sample.",
        "required": ["sample_name", "assay_type", "library_prep_date"],
        "optional": ["library_protocol", "library_version"],
        "system":   ["id", "sample_id", "created_at", "updated_at", "extra_metadata"],
        "relations": ["samples", "flowcell_libraries", "pool_members"],
        "pos":      {"x": 185, "y": 360},
    },

    "pools": {
        "label":    "Pools",
        "color":    "#fb7185",
        "colorBg":  "#200b10",
        "desc":     "A physical pooling of experiment libraries before sequencing.",
        "required": ["pool_name"],
        "optional": ["description"],
        "system":   ["id", "created_at", "updated_at", "extra_metadata"],
        "relations": ["pool_members"],
        "pos":      {"x": 510, "y": 425},
    },

    "pool_members": {
        "label":       "Pool members",
        "color":       "#fb7185",
        "colorBg":     "#1a080c",
        "desc":        "Junction. Links experiments to pools.",
        "required":    ["pool_name", "sample_name", "assay_type", "library_prep_date"],
        "optional":    [],
        "system":      ["pool_id", "experiment_id", "added_at"],
        "relations":   ["pools", "experiments"],
        "pos":         {"x": 370, "y": 480},
        "no_metadata": True,
    },

    "sequencing_runs": {
        "label":    "Sequencing runs",
        "color":    "#94a3b8",
        "colorBg":  "#141920",
        "desc":     "A sequencing flowcell or run. BCL output can be linked via bcl_gcs_uri.",
        "required": ["flowcell_id"],
        "optional": ["machine", "run_date", "read_length", "sequencing_center", "bcl_gcs_uri"],
        "system":   ["id", "created_at", "extra_metadata"],
        "relations": ["flowcell_libraries"],
        "pos":      {"x": 40, "y": 610},
    },

    "flowcell_libraries": {
        "label":    "Flowcell libraries",
        "color":    "#94a3b8",
        "colorBg":  "#141920",
        "desc":     "Pre-registers lane and index assignments for each experiment on a sequencing run.",
        "required": ["sample_name", "assay_type", "library_prep_date", "flowcell_id", "lane", "index_sequence"],
        "optional": [],
        "system":   ["id", "experiment_id", "run_id", "created_at", "updated_at", "extra_metadata"],
        "relations": ["experiments", "sequencing_runs", "files"],
        "pos":      {"x": 185, "y": 490},
    },

    "files": {
        "label":    "Files",
        "color":    "#94a3b8",
        "colorBg":  "#141920",
        "desc":     "Physical outputs — FASTQ, BAM, count matrices. Stored in GCS or cluster paths.",
        "required": ["sample_name", "assay_type", "library_prep_date", "flowcell_id", "file_type"],
        "optional": ["gcs_uri", "gcs_bucket", "file_path", "file_format", "subject_id"],
        "system":   ["id", "flowcell_library_id", "created_at", "updated_at", "extra_metadata"],
        "relations": ["flowcell_libraries"],
        "pos":      {"x": 330, "y": 610},
    },

}

EDGES = [
    ("projects",          "samples"),
    ("subjects",          "sample_sources"),
    ("samples",           "sample_sources"),
    ("samples",           "experiments"),
    ("samples",           "cohort_members"),
    ("cohorts",           "cohort_members"),
    ("experiments",       "pool_members"),
    ("pools",             "pool_members"),
    ("experiments",       "flowcell_libraries"),
    ("sequencing_runs",   "flowcell_libraries"),
    ("flowcell_libraries","files"),
]
