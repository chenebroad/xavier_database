import streamlit as st
import pandas as pd
import json
from api_client import create_project, create_sample, create_experiment, create_run, create_seqexp, create_file, create_cohort, create_cohort_member, create_pool, create_pool_member
import math

ENTITY_SCHEMAS = {
    "projects": {
        "core": ["project_name", "description"],
        "api": create_project
    },
    "samples": {
        "core": ["sample_name", "project_name", "subject_id", "status", "organism", "tissue"],
        "api": create_sample
    },
    "experiments": {
        "core": ["sample_name", "assay_type", "library_prep_date", "library_protocol", "library_version"],
        "api": create_experiment
    },
    "sequencing_runs": {
        "core": ["flowcell_id", "machine", "run_date", "read_length", "sequencing_center"],
        "api": create_run
    },
    "seqexp": {
        "core": ["sample_name", "assay_type", "library_prep_date", "flowcell_id", "lane", "index_sequence"],
        "api": create_seqexp
    },
    "files": {
        "core": ["sample_name", "assay_type", "library_prep_date", "flowcell_id", "lane",
                 "gcs_uri", "gcs_bucket", "file_path", "size_bytes",
                 "file_type", "file_format", "checksum_md5"],
        "api": create_file
    },
    "cohorts": {
        "core": ["cohort_name", "cohort_type"],
        "api": create_cohort
    },
    "cohort_members": {
        "core": ["cohort_name", "sample_name"],
        "api": create_cohort_member,
        "no_metadata": True
    },
    "pools": {
        "core": ["pool_name"],
        "api": create_pool
    },
    "pool_members": {
        "core": ["pool_name", "sample_name", "assay_type", "library_prep_date"],
        "api": create_pool_member,
        "no_metadata": True
    },
}

st.title("📥 Ingest Data")

tab1, tab2 = st.tabs(["Upload CSV", "Manual Entry"])

#HELPER FUNCTIONS

def sanitize_payload(obj):
    if isinstance(obj, dict):
        return {k: sanitize_payload(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [sanitize_payload(v) for v in obj]
    elif isinstance(obj, float):
        if math.isnan(obj) or math.isinf(obj):
            return None
    return obj


def build_payload(row_dict, core_columns, no_metadata=False):
    core = {}
    metadata = {}

    for k, v in row_dict.items():
        v = None if pd.isna(v) else v

        if k in core_columns:
            core[k] = v
        elif not no_metadata and v not in ["", None]:
            metadata[k] = v

    if not no_metadata:
        core["extra_metadata"] = metadata

    return sanitize_payload(core)


def validate_payload(payload, core_columns):
    errors = []

    for col in core_columns:
        if col not in payload or payload[col] in [None, ""]:
            errors.append(f"Missing required field: {col}")

    return errors

# -------------------------
# CSV UPLOAD
# -------------------------
with tab1:
    st.subheader("Upload CSV")

    entity = st.selectbox(
        "Entity Type",
        list(ENTITY_SCHEMAS.keys()),
        key="entity_tab1"
    )

    core_columns = ENTITY_SCHEMAS[entity]["core"]
    st.write(f"Core columns: {', '.join(core_columns)}")
    api_fn = ENTITY_SCHEMAS[entity]["api"]

    uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

    if uploaded_file:
        df = pd.read_csv(uploaded_file)

        st.write("Preview:")
        st.dataframe(df)

        if st.button("Validate CSV"):
            all_errors = []

            for i, row in df.iterrows():
                payload = build_payload(row.to_dict(), core_columns)
                errors = validate_payload(payload, core_columns)

                if errors:
                    all_errors.append({"row": i, "errors": errors})

            if all_errors:
                st.error("Validation errors found")
                st.json(all_errors)
            else:
                st.success("CSV validation passed")

        if st.button("Submit All Rows"):
            success = 0
            errors = []

            for i, row in df.iterrows():
                payload = build_payload(row.to_dict(), core_columns)

                try:
                    api_fn(payload)
                    success += 1

                except Exception as e:
                    errors.append({"row": i, "error": str(e)})

            st.success(f"{success} rows inserted")

            if errors:
                st.error("Errors:")
                st.json(errors)


# -------------------------
# MANUAL ENTRY
# -------------------------
with tab2:

    entity = st.selectbox(
        "Entity Type",
        list(ENTITY_SCHEMAS.keys()),
        key="entity_tab2"
    )

    core_columns = ENTITY_SCHEMAS[entity]["core"]
    api_fn = ENTITY_SCHEMAS[entity]["api"]

    st.write(f"Editing: {entity}")

    # metadata builder (keep for now, but now isolated)
    st.subheader("Metadata Fields")

    if "metadata_fields" not in st.session_state:
        st.session_state.metadata_fields = []

    new_field = st.text_input("Add metadata field")

    if st.button("Add Field"):
        if new_field and new_field not in st.session_state.metadata_fields:
            st.session_state.metadata_fields.append(new_field)

    all_columns = core_columns + st.session_state.metadata_fields

    df_template = pd.DataFrame([{col: "" for col in all_columns}])

    edited_df = st.data_editor(
        df_template,
        num_rows="dynamic",
        use_container_width=True
    )

    if st.button("Validate"):
        errors = []

        for i, row in edited_df.iterrows():
            row_dict = row.to_dict()

            if all(v in ["", None] for v in row_dict.values()):
                continue

            payload = build_payload(row_dict, core_columns)
            row_errors = validate_payload(payload, core_columns)

            if row_errors:
                errors.append({"row": i, "errors": row_errors})

        if errors:
            st.error("Validation issues found")
            st.json(errors)
        else:
            st.success("All rows valid")

    if st.button("Submit Data"):
        success = 0
        errors = []

        for i, row in edited_df.iterrows():

            row_dict = row.to_dict()

            if all(v in ["", None] for v in row_dict.values()):
                continue

            payload = build_payload(row_dict, core_columns)

            try:
                api_fn(payload)
                success += 1

            except Exception as e:
                errors.append({"row": i, "error": str(e)})

        st.success(f"{success} rows inserted")

        if errors:
            st.error("Some rows failed")
            st.json(errors)