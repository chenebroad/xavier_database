import streamlit as st
import pandas as pd
from api_client import query_data, run_quick_query, update_row

# =====================================================
# CONFIG
# =====================================================

TABLES = {
    "projects": {"editable": True},
    "samples": {"editable": True},
    "experiments": {"editable": True},
    "sequencing_runs": {"editable": True},
    "run_experiments": {"editable": False},
    "seqexp": {"editable": True},
    "files": {"editable": True}
}

QUICK_QUERIES = {
    "All Samples from Project": {
        "endpoint": "samples_by_project",
        "params": ["project_name"]
    },
    "All Experiments from Sample": {
        "endpoint": "experiments_by_sample",
        "params": ["sample_name"]
    },
    "All Files from Sample": {
        "endpoint": "files_by_sample",
        "params": ["sample_name"]
    },
    "All Files from Project": {
        "endpoint": "files_by_project",
        "params": ["project_name"]
    }
}

# =====================================================
# SESSION STATE
# =====================================================

if "query_results" not in st.session_state:
    st.session_state.query_results = None

if "edited_df" not in st.session_state:
    st.session_state.edited_df = None

if "original_df" not in st.session_state:
    st.session_state.original_df = None

# =====================================================
# HELPERS
# =====================================================

def normalize(row):
    return {
        k: (None if v == "" else v)
        for k, v in row.items()
    }

# =====================================================
# PAGE OPTIONS
# =====================================================

edit_data = st.toggle("Edit Data")

tab1, tab2, tab3 = st.tabs(
    [
        "Browse Data",
        "Quick Queries",
        "Custom Query"
    ]
)

# =====================================================
# TAB 1 - BROWSE DATA
# =====================================================

st.header("🔍 Query Data")

with tab1:

    st.subheader("Browse Database Tables")

    selected_table = st.selectbox(
        "Select Table",
        list(TABLES.keys())
    )

    limit = st.number_input(
        "Row Limit",
        min_value=1,
        max_value=10000,
        value=100
    )

    # -------------------------
    # QUERY
    # -------------------------

    if st.button("Run Query"):

        try:

            data = query_data(
                selected_table,
                limit
            )

            if not data:

                st.warning("No data found")

                st.session_state.query_results = None
                st.session_state.edited_df = None
                st.session_state.original_df = None

            else:

                df = pd.DataFrame(data)

                st.session_state.query_results = df
                st.session_state.edited_df = df.copy()
                st.session_state.original_df = df.copy()

        except Exception as e:

            st.error("Query failed")
            st.write(e)

    # -------------------------
    # DISPLAY RESULTS
    # -------------------------

    if st.session_state.query_results is not None:

        df = st.session_state.query_results.copy()

        # -------------------------
        # FILTERS
        # -------------------------

        st.subheader("Filters")

        col1, col2 = st.columns(2)

        with col1:
            filter_column = st.selectbox(
                "Filter Column",
                [""] + list(df.columns)
            )

        with col2:
            filter_value = st.text_input(
                "Contains Value"
            )

        if filter_column and filter_value:

            df = df[
                df[filter_column]
                .astype(str)
                .str.contains(
                    filter_value,
                    case=False,
                    na=False
                )
            ]

        # -------------------------
        # COLUMN SELECTION
        # -------------------------

        selected_columns = st.multiselect(
            "Columns to Display",
            list(df.columns),
            default=list(df.columns)
        )

        if selected_columns:
            df = df[selected_columns]

        # -------------------------
        # METRICS
        # -------------------------

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Rows Returned",
                len(df)
            )

        with col2:
            st.metric(
                "Columns Displayed",
                len(df.columns)
            )

        # -------------------------
        # DOWNLOAD
        # -------------------------

        csv = df.to_csv(index=False).encode("utf-8")

        st.download_button(
            "⬇️ Download Results",
            csv,
            f"{selected_table}.csv",
            "text/csv"
        )

        # =====================================================
        # EDIT MODE
        # =====================================================

        if edit_data and TABLES[selected_table]["editable"]:

            st.subheader("✏️ Edit Data")

            edited_df = st.data_editor(
                st.session_state.edited_df,
                use_container_width=True,
                num_rows="fixed",
                key="data_editor"
            )

            if not edited_df.equals(
                st.session_state.edited_df
            ):
                st.session_state.edited_df = edited_df

            # -------------------------
            # SHOW CHANGE COUNT
            # -------------------------

            changed_rows = []

            original_df = st.session_state.original_df

            for i in range(len(edited_df)):

                original = original_df.iloc[i].to_dict()
                edited = edited_df.iloc[i].to_dict()

                if normalize(original) != normalize(edited):
                    changed_rows.append(i)

            st.info(
                f"{len(changed_rows)} rows modified"
            )

            # -------------------------
            # OPTIONAL CSV RE-UPLOAD
            # -------------------------

            st.subheader("Upload Edited CSV")

            uploaded_file = st.file_uploader(
                "Upload CSV",
                type=["csv"]
            )

            if uploaded_file:

                try:

                    edited_df = pd.read_csv(
                        uploaded_file
                    )

                    st.write(
                        "Preview uploaded data"
                    )

                    st.dataframe(
                        edited_df,
                        use_container_width=True
                    )

                except Exception as e:

                    st.error(
                        f"Failed to read CSV: {e}"
                    )

            # -------------------------
            # APPLY CHANGES
            # -------------------------

            if st.button("Apply Uploaded Changes"):

                errors = []

                changes_made = False

                for i in range(len(edited_df)):

                    original = original_df.iloc[i].to_dict()
                    edited = edited_df.iloc[i].to_dict()

                    if normalize(original) != normalize(edited):

                        changes_made = True

                        row_id = original.get("id")

                        payload = {
                            k: (
                                None
                                if v == ""
                                else v
                            )
                            for k, v in edited.items()
                            if k not in [
                                "id",
                                "created_at",
                                "updated_at"
                            ]
                        }

                        try:

                            update_row(
                                selected_table,
                                row_id,
                                payload
                            )

                        except Exception as e:

                            errors.append(
                                {
                                    "row": i,
                                    "error": str(e)
                                }
                            )

                if errors:

                    st.error(
                        "Some rows failed:"
                    )

                    st.json(errors)

                elif changes_made:

                    st.success(
                        "Changes applied successfully"
                    )

                    refreshed = query_data(
                        selected_table,
                        limit
                    )

                    st.session_state.query_results = (
                        pd.DataFrame(refreshed)
                    )

                else:

                    st.info(
                        "No changes detected"
                    )

        # =====================================================
        # VIEW MODE
        # =====================================================

        else:

            st.subheader("📄 View Data")

            st.dataframe(
                df,
                use_container_width=True
            )

# =====================================================
# TAB 2 - QUICK QUERIES
# =====================================================

with tab2:

    st.subheader("⚡ Quick Queries")

    query_name = st.selectbox(
        "Select Query",
        list(QUICK_QUERIES.keys())
    )

    params = {}

    for param in QUICK_QUERIES[query_name]["params"]:

        params[param] = st.text_input(
            param.replace(
                "_",
                " "
            ).title()
        )

    if st.button("Run Quick Query"):

        try:

            data = run_quick_query(
                QUICK_QUERIES[query_name]["endpoint"],
                **params
            )

            df = pd.DataFrame(data)

            if df.empty:

                st.warning(
                    "No results found"
                )

            else:

                st.success(
                    f"{len(df)} rows returned"
                )

                st.dataframe(
                    df,
                    use_container_width=True
                )

        except Exception as e:

            st.error(
                "Query failed"
            )

            st.write(e)

with tab3:
    sql = st.text_area(
        "SQL Query",
        height=200
    )

    if st.button("Run SQL"):
        data = run_sql_query(sql)
        df = pd.DataFrame(data)
        st.dataframe(df)