import streamlit as st
import pandas as pd
import json
from api_client import (
    create_project, create_sample, create_experiment,
    create_run, create_seqexp, create_file,
    create_cohort, create_cohort_member,
    create_pool, create_pool_member
)
import math

ENTITY_SCHEMAS = {
    "projects": {
        "required": ["project_name"],
        "optional": ["description"],
        "api": create_project
    },
    "samples": {
        "required": ["sample_name", "project_name", "organism", "tissue"],
        "optional": ["sample_type", "status"],
        "api": create_sample
    },
    "experiments": {
        "required": ["sample_name", "assay_type", "library_prep_date"],
        "optional": ["library_protocol", "library_version"],
        "api": create_experiment
    },
    "sequencing_runs": {
        "required": ["flowcell_id", "machine", "run_date", "read_length"],
        "optional": ["sequencing_center"],
        "api": create_run
    },
    "seqexp": {
        "required": ["sample_name", "assay_type", "library_prep_date", "flowcell_id", "lane", "index_sequence"],
        "optional": [],
        "api": create_seqexp
    },
    "files": {
        "required": ["sample_name", "assay_type", "library_prep_date", "flowcell_id",
                     "gcs_uri", "file_type", "file_format", "checksum_md5"],
        "optional": ["lane", "gcs_bucket", "file_path", "size_bytes"],
        "api": create_file
    },
    "cohorts": {
        "required": ["cohort_name"],
        "optional": ["cohort_type"],
        "api": create_cohort
    },
    "cohort_members": {
        "required": ["cohort_name", "sample_name"],
        "optional": [],
        "api": create_cohort_member,
        "no_metadata": True
    },
    "pools": {
        "required": ["pool_name"],
        "optional": [],
        "api": create_pool
    },
    "pool_members": {
        "required": ["pool_name", "sample_name", "assay_type", "library_prep_date"],
        "optional": [],
        "api": create_pool_member,
        "no_metadata": True
    },
}

st.title("📥 Ingest Data")

tab1, tab2 = st.tabs(["Upload CSV", "Manual Entry"])

# ── Helper functions ──────────────────────────────────────────────────────────

def sanitize_payload(obj):
    if isinstance(obj, dict):
        return {k: sanitize_payload(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [sanitize_payload(v) for v in obj]
    elif isinstance(obj, float):
        if math.isnan(obj) or math.isinf(obj):
            return None
    return obj


def build_payload(row_dict, required_columns, optional_columns, no_metadata=False):
    core = {}
    metadata = {}
    all_core = required_columns + optional_columns

    for k, v in row_dict.items():
        v = None if pd.isna(v) else v

        if k in all_core:
            core[k] = v
        elif not no_metadata and v not in ["", None]:
            metadata[k] = v

    if not no_metadata:
        core["extra_metadata"] = metadata

    return sanitize_payload(core)


def validate_payload(payload, required_columns):
    errors = []
    for col in required_columns:
        if col not in payload or payload[col] in [None, ""]:
            errors.append(f"Missing required field: {col}")
    return errors


def schema_helper(entity):
    """Renders required / optional field info for the selected entity."""
    schema = ENTITY_SCHEMAS[entity]
    required = schema["required"]
    optional = schema["optional"]

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Required fields**")
        for f in required:
            st.markdown(f"- `{f}`")

    with col2:
        st.markdown("**Optional fields**")
        if optional:
            for f in optional:
                st.markdown(f"- `{f}`")
        else:
            st.markdown("_None_")

    if not schema.get("no_metadata"):
        st.caption("Any additional columns in your CSV will be stored in extra_metadata.")

# ── CSV Upload ────────────────────────────────────────────────────────────────

with tab1:
    st.subheader("Upload CSV")

    entity = st.selectbox(
        "Entity type",
        list(ENTITY_SCHEMAS.keys()),
        key="entity_tab1"
    )

    schema        = ENTITY_SCHEMAS[entity]
    required_cols = schema["required"]
    optional_cols = schema["optional"]
    no_metadata   = schema.get("no_metadata", False)
    api_fn        = schema["api"]

    schema_helper(entity)
    st.divider()

    uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

    if uploaded_file:
        df = pd.read_csv(uploaded_file)

        st.write("Preview:")
        st.dataframe(df)

        if st.button("Validate CSV"):
            all_errors = []

            for i, row in df.iterrows():
                payload = build_payload(
                    row.to_dict(), required_cols, optional_cols, no_metadata
                )
                errors = validate_payload(payload, required_cols)

                if errors:
                    all_errors.append({"row": i, "errors": errors})

            if all_errors:
                st.error("Validation errors found")
                st.json(all_errors)
            else:
                st.success("CSV validation passed")

        if st.button("Submit all rows"):
            success = 0
            errors  = []

            for i, row in df.iterrows():
                payload = build_payload(
                    row.to_dict(), required_cols, optional_cols, no_metadata
                )

                try:
                    api_fn(payload)
                    success += 1
                except Exception as e:
                    errors.append({"row": i, "error": str(e)})

            st.success(f"{success} rows inserted")

            if errors:
                st.error("Errors:")
                st.json(errors)


# ── Manual Entry ──────────────────────────────────────────────────────────────

with tab2:

    entity = st.selectbox(
        "Entity type",
        list(ENTITY_SCHEMAS.keys()),
        key="entity_tab2"
    )

    schema        = ENTITY_SCHEMAS[entity]
    required_cols = schema["required"]
    optional_cols = schema["optional"]
    no_metadata   = schema.get("no_metadata", False)
    api_fn        = schema["api"]

    schema_helper(entity)
    st.divider()

    if "metadata_fields" not in st.session_state:
        st.session_state.metadata_fields = []

    if not no_metadata:
        st.subheader("Extra metadata fields")
        new_field = st.text_input("Add metadata field")

        if st.button("Add field"):
            if new_field and new_field not in st.session_state.metadata_fields:
                st.session_state.metadata_fields.append(new_field)

    all_columns  = required_cols + optional_cols
    if not no_metadata:
        all_columns += st.session_state.metadata_fields

    df_template = pd.DataFrame([{col: "" for col in all_columns}])

    edited_df = st.data_editor(
        df_template,
        num_rows="dynamic",
        use_container_width=True,
        column_config={
            col: st.column_config.TextColumn(
                col,
                help="Required" if col in required_cols else "Optional"
            )
            for col in all_columns
        }
    )

    if st.button("Validate"):
        errors = []

        for i, row in edited_df.iterrows():
            row_dict = row.to_dict()

            if all(v in ["", None] for v in row_dict.values()):
                continue

            payload    = build_payload(row_dict, required_cols, optional_cols, no_metadata)
            row_errors = validate_payload(payload, required_cols)

            if row_errors:
                errors.append({"row": i, "errors": row_errors})

        if errors:
            st.error("Validation issues found")
            st.json(errors)
        else:
            st.success("All rows valid")

    if st.button("Submit data"):
        success = 0
        errors  = []

        for i, row in edited_df.iterrows():
            row_dict = row.to_dict()

            if all(v in ["", None] for v in row_dict.values()):
                continue

            payload = build_payload(row_dict, required_cols, optional_cols, no_metadata)

            try:
                api_fn(payload)
                success += 1
            except Exception as e:
                errors.append({"row": i, "error": str(e)})

        st.success(f"{success} rows inserted")

        if errors:
            st.error("Some rows failed")
            st.json(errors)