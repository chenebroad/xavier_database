import streamlit as st
import pandas as pd
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from api_client import get_metadata_registry, create_registry_entry, deprecate_registry_entry

ENTITY_TYPES = [
    "projects", "subjects", "samples", "cohorts", "experiments",
    "pools", "sequencing_runs", "flowcell_libraries", "files",
]

DATA_TYPES = ["text", "integer", "float", "boolean", "enum"]

st.title("Metadata Registry")
st.caption(
    "The registry tracks custom extra_metadata fields used across entity types. "
    "Fields listed here are soft-validated on ingest — unknown keys still pass through. "
    "Register a field so other groups know it exists and what values are expected."
)

tab1, tab2 = st.tabs(["Browse Registry", "Register a Field"])

# ── Browse ────────────────────────────────────────────────────────────────────

with tab1:
    entity_filter = st.selectbox(
        "Filter by entity type",
        ["All"] + ENTITY_TYPES,
        key="registry_filter"
    )

    try:
        et = None if entity_filter == "All" else entity_filter
        rows = get_metadata_registry(entity_type=et)

        if rows:
            df = pd.DataFrame(rows)

            # Friendlier column order
            show_cols = [c for c in
                ["entity_type", "field_name", "data_type", "required",
                 "allowed_values", "description", "deprecated", "created_at", "id"]
                if c in df.columns]
            df = df[show_cols]

            # Deprecate action
            if st.toggle("Show deprecate controls", value=False):
                for _, row in df[~df["deprecated"]].iterrows():
                    col1, col2 = st.columns([4, 1])
                    with col1:
                        st.markdown(
                            f"**{row['entity_type']}** · `{row['field_name']}` "
                            f"({row['data_type']})"
                            + (f" — {row['description']}" if row.get("description") else "")
                        )
                    with col2:
                        if st.button("Deprecate", key=f"dep_{row['id']}"):
                            try:
                                deprecate_registry_entry(row["id"])
                                st.success(f"Deprecated '{row['field_name']}'")
                                st.rerun()
                            except Exception as e:
                                st.error(str(e))
            else:
                st.dataframe(
                    df[~df["deprecated"]],
                    use_container_width=True,
                    hide_index=True,
                )

                with st.expander("Show deprecated fields"):
                    dep = df[df["deprecated"]]
                    if dep.empty:
                        st.caption("None")
                    else:
                        st.dataframe(dep, use_container_width=True, hide_index=True)

        else:
            st.info("No registry entries yet. Use the **Register a Field** tab to add the first one.")

    except Exception as e:
        st.error(f"Could not load registry: {e}")

# ── Register ──────────────────────────────────────────────────────────────────

with tab2:
    st.subheader("Register a new metadata field")
    st.caption(
        "Use this form to document a custom field your group tracks in extra_metadata. "
        "Once registered, ingest will type-check and value-check this field on new submissions."
    )

    with st.form("register_field"):
        entity_type = st.selectbox("Entity type", ENTITY_TYPES)
        field_name  = st.text_input("Field name", placeholder="e.g. inflammation_score")
        data_type   = st.selectbox("Data type", DATA_TYPES)
        description = st.text_area("Description", placeholder="What does this field represent?")
        required    = st.checkbox("Required field")

        allowed_values_raw = ""
        if data_type == "enum":
            allowed_values_raw = st.text_input(
                "Allowed values (comma-separated)",
                placeholder="mild, moderate, severe"
            )

        submitted = st.form_submit_button("Register field")

    if submitted:
        if not field_name.strip():
            st.error("Field name is required.")
        else:
            allowed_values = None
            if data_type == "enum":
                allowed_values = [v.strip() for v in allowed_values_raw.split(",") if v.strip()]
                if not allowed_values:
                    st.error("Provide at least one allowed value for enum fields.")
                    st.stop()

            payload = {
                "entity_type":    entity_type,
                "field_name":     field_name.strip(),
                "data_type":      data_type,
                "required":       required,
                "description":    description.strip() or None,
                "allowed_values": allowed_values,
            }

            try:
                create_registry_entry(payload)
                st.success(
                    f"Registered **{field_name}** on **{entity_type}**. "
                    "Future submissions will be validated against this entry."
                )
            except Exception as e:
                st.error(str(e))
