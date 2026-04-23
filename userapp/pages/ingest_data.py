import streamlit as st
import pandas as pd
import json
from api_client import create_project, create_sample, create_experiment, create_run, create_seqexp, create_file
import math
st.title("📥 Ingest Data")

tab1, tab2 = st.tabs(["Upload CSV", "Manual Entry"])

def sanitize_payload(obj):
    if isinstance(obj, dict):
        return {k: sanitize_payload(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [sanitize_payload(v) for v in obj]
    elif isinstance(obj, float):
        if math.isnan(obj) or math.isinf(obj):
            return None
    return obj

# -------------------------
# CSV UPLOAD
# -------------------------
with tab1:
    st.subheader("Upload CSV")

    entity_tab1 = st.selectbox("Entity Type", 
                               ["projects", "samples", "experiments", "sequencing_runs", "seqexp", "files"],
                               key="entity_tab1")

    match entity_tab1:
        case "projects":
            core_columns = ["project_name", "description"]

        case "samples":
            core_columns = ["project_name", "sample_name", "subject_id", "status", "organism", "tissue"]

        case "experiments":
            core_columns = ["sample_name", "assay_type", "library_prep_date",
                            "library_protocol", "library_version"]

        case "sequencing_runs":
            core_columns = ["flowcell_id", "machine", "run_date",
                            "read_length", "sequencing_center"]

        case "seqexp":
            core_columns = ["sample_name", "assay_type", "library_prep_date", "flowcell_id",
                            "lane", "index_sequence"]

        case "files":
            core_columns = ["sample_name", "assay_type", "library_prep_date", "flowcell_id", "lane",
                            "gcs_uri", "gcs_bucket", "file_path", "size_bytes",
                             "file_type", "file_format", "checksum_md5"]

    uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

    if uploaded_file:
        df = pd.read_csv(uploaded_file)

        st.write("Preview:")
        st.dataframe(df)

        if st.button("Submit All Rows"):
            success = 0
            errors = []

            for i, row in df.iterrows():
                payload = {}
                payload["extra_metadata"] = {}

                try:
                    for col in df.columns:
                        val = row[col]
                        val = None if pd.isna(val) else val
                        
                        if col in core_columns:
                            payload[col] = row[col]
                        else:
                            payload["extra_metadata"][col] = val
                    
                    payload = sanitize_payload(payload)

                    match entity_tab1:
                        case "projects":
                            create_project(payload)

                        case "samples":
                            create_sample(payload)

                        case "experiments":
                            create_experiment(payload)

                        case "sequencing_runs":
                            create_run(payload)

                        case "seqexp":
                            create_seqexp(payload)

                        case "files":
                            create_file(payload)

                    success += 1

                except Exception as e:
                    errors.append({"row": i, "error": str(e)})

            st.success(f"{success} rows inserted")

            if errors:
                st.error("Errors:")
                st.write(errors)


# -------------------------
# MANUAL ENTRY
# -------------------------
with tab2:

    entity_tab2 = st.selectbox(
        "Entity Type",
        ["projects", "samples", "experiments", "sequencing_runs", "seqexp", "files"],
        key="entity_tab2"
    )

    st.write(f"You have chosen to submit {entity_tab2}, edit the table below:")

    # -------------------------
    # METADATA FIELD BUILDER
    # -------------------------
    st.subheader("Add additional Metadata Fields")

    new_field = st.text_input("New metadata column name")

    if "metadata_fields" not in st.session_state:
        st.session_state.metadata_fields = []

    if st.button("Add Field"):
        if new_field and new_field not in st.session_state.metadata_fields:
            st.session_state.metadata_fields.append(new_field)

    # Show current metadata fields
    if st.session_state.metadata_fields:
        st.write("Current metadata fields:", st.session_state.metadata_fields)

    # -------------------------
    # CORE COLUMN DEFINITIONS
    # -------------------------
    match entity_tab2:
        case "projects":
            core_columns = ["project_name", "description"]

        case "samples":
            core_columns = ["sample_name", "subject_id", "status", "organism", "tissue"]

        case "experiments":
            core_columns = ["sample_name", "assay_type", "library_prep_date",
                            "library_protocol", "library_version"]

        case "seqexp":
            core_columns = ["sample_name", "assay_type", "library_prep_date", "flowcell_id",
                            "lane", "index_sequence"]

        case "sequencing_runs":
            core_columns = ["flowcell_id", "machine", "run_date",
                            "read_length", "sequencing_center"]

        case "files":
            core_columns = ["sample_name", "assay_type", "library_prep_date", "flowcell_id", "lane",
                            "gcs_uri", "gcs_bucket", "file_path", "size_bytes",
                             "file_type", "file_format", "checksum_md5"]

    all_columns = core_columns + st.session_state.metadata_fields

    df_template = pd.DataFrame([{col: "" for col in all_columns}])

    edited_df = st.data_editor(
        df_template,
        num_rows="dynamic",
        use_container_width=True
    )

    # -------------------------
    # SUBMIT BUTTON
    # -------------------------
    if st.button("Submit Data"):
        success = 0
        errors = []

        for i, row in edited_df.iterrows():

            row_dict = row.to_dict()

            # Skip completely empty rows
            if all(v in ["", None] for v in row_dict.values()):
                continue

            # -------------------------
            # SPLIT CORE + METADATA
            # -------------------------
            core_data = {}
            metadata = {}

            for key, value in row_dict.items():
                if key in core_columns:
                    core_data[key] = value
                else:
                    if value not in ["", None]:
                        metadata[key] = value

            core_data["extra_metadata"] = metadata
            core_data = sanitize_payload(core_data)
            
            # -------------------------
            # API ROUTING
            # -------------------------
            try:
                match entity_tab2:
                    case "samples":
                        create_sample(core_data)

                    case "projects":
                        create_project(core_data)

                    case "experiments":
                        create_experiment(core_data)

                    case "sequencing_runs":
                        create_run(core_data)

                    case "seqexp":
                        create_seqexp(core_data)

                    case "files":
                        create_file(core_data)

                success += 1

            except Exception as e:
                err_info = e.args[0] if isinstance(e.args[0], dict) else {"error_msg": str(e), "payload": row_dict}
                errors.append({
                    "row": i,
                    "error_type": err_info.get("error_type", ""),
                    "error_msg": err_info.get("error_msg", ""),
                    "payload": err_info.get("payload", row_dict)
                })

        st.success(f"{success} rows inserted")

        if errors:
            st.error("Some rows failed to ingest:")
            for err in errors:
                st.write(f"Row {err['row']}")
                st.error(f"{err['error_type']}: {err['error_msg']}")
                st.json(err['payload'])