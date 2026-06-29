import json
import streamlit as st
import pandas as pd
from api_client import query_data, run_quick_query, update_row

st.header("🔍 Query Data")

# =====================================================
# CONFIG
# =====================================================

TABLES = {
    "projects":        {"editable": True},
    "subjects":        {"editable": True},
    "samples":         {"editable": True},
    "sample_sources":  {"editable": False},  # junction
    "cohorts":         {"editable": True},
    "cohort_members":  {"editable": False},  # junction
    "experiments":     {"editable": True},
    "pools":           {"editable": True},
    "pool_members":    {"editable": False},  # junction
    "sequencing_runs": {"editable": True},
    "run_experiments": {"editable": False},  # junction
    "files":           {"editable": True},
}

QUICK_QUERIES = {
    "All Samples from Project": {
        "endpoint": "samples_by_project",
        "params":   ["project_name"]
    },
    "All Experiments from Sample": {
        "endpoint": "experiments_by_sample",
        "params":   ["sample_name"]
    },
    "All Files from Sample": {
        "endpoint": "files_by_sample",
        "params":   ["sample_name"]
    },
    "All Files from Project": {
        "endpoint": "files_by_project",
        "params":   ["project_name"]
    },
    "All Samples from Cohort": {
        "endpoint": "samples_by_cohort",
        "params":   ["cohort_name"]
    },
    "All Subjects from Sample": {
        "endpoint": "subjects_by_sample",
        "params":   ["sample_name"]
    },
    "All Experiments from Pool": {
        "endpoint": "experiments_by_pool",
        "params":   ["pool_name"]
    },
}

# =====================================================
# SESSION STATE
# =====================================================

for key in ["query_results", "original_df", "pending_changes"]:
    if key not in st.session_state:
        st.session_state[key] = None

# =====================================================
# HELPERS
# =====================================================

def normalize_value(v):
    """
    Normalize a value for comparison.
    Handles dict/string inconsistencies that arise when
    JSONB columns are serialized differently by pandas vs the API.
    """
    if v is None or v == "":
        return None
    if isinstance(v, dict):
        return json.dumps(v, sort_keys=True)
    if isinstance(v, str):
        stripped = v.strip()
        # Attempt to parse stringified dicts/JSON for consistent comparison
        try:
            parsed = json.loads(stripped.replace("'", '"'))
            return json.dumps(parsed, sort_keys=True)
        except Exception:
            return stripped
    return v


def compute_changes_from_editor(editor_key: str, original_df: pd.DataFrame) -> list[dict]:
    """
    Read changes directly from data_editor's built-in state.
    data_editor stores only actually-edited rows under
    st.session_state[editor_key]["edited_rows"] as:
        { "row_index": { "field": new_value, ... }, ... }
    This avoids full-dataframe diffing and eliminates false positives.
    """
    editor_state = st.session_state.get(editor_key)
    if not editor_state:
        return []

    raw_edits = editor_state.get("edited_rows", {})
    changes   = []

    for row_idx_str, field_changes in raw_edits.items():
        row_idx     = int(row_idx_str)
        original_row = original_df.iloc[row_idx].to_dict()

        for field, new_val in field_changes.items():
            if field in ["id", "created_at", "updated_at", "added_at"]:
                continue
            orig_val = original_row.get(field)
            if normalize_value(orig_val) != normalize_value(new_val):
                changes.append({
                    "row":   row_idx,
                    "field": field,
                    "from":  orig_val,
                    "to":    new_val,
                    "id":    original_row.get("id"),
                })

    return changes


def compute_changes_from_csv(original_df: pd.DataFrame, uploaded_df: pd.DataFrame) -> list[dict]:
    """
    Diff for the CSV upload path — compares full dataframes
    but uses normalize_value to avoid JSONB false positives.
    """
    changes = []
    for i in range(min(len(original_df), len(uploaded_df))):
        original_row = original_df.iloc[i].to_dict()
        edited_row   = uploaded_df.iloc[i].to_dict()
        for field in edited_row:
            if field in ["id", "created_at", "updated_at", "added_at"]:
                continue
            if normalize_value(original_row.get(field)) != normalize_value(edited_row.get(field)):
                changes.append({
                    "row":   i,
                    "field": field,
                    "from":  original_row.get(field),
                    "to":    edited_row.get(field),
                    "id":    original_row.get("id"),
                })
    return changes


def apply_changes(changes: list[dict], table: str) -> tuple[int, list[dict]]:
    """
    Group field-level changes by row ID then fire one PATCH per row.
    Returns (success_count, errors).
    """
    rows_to_patch: dict[str, dict] = {}
    for change in changes:
        row_id = change["id"]
        if row_id not in rows_to_patch:
            rows_to_patch[row_id] = {}
        rows_to_patch[row_id][change["field"]] = change["to"]

    success, errors = 0, []
    for row_id, payload in rows_to_patch.items():
        try:
            update_row(table, row_id, payload)
            success += 1
        except Exception as e:
            errors.append({"id": row_id, "error": str(e)})
    return success, errors


def show_pending_changes(changes: list[dict]) -> None:
    """Render the change preview table."""
    change_df = pd.DataFrame(changes)[["row", "field", "from", "to"]]
    st.dataframe(change_df, use_container_width=True, hide_index=True)
    st.caption(
        f"{len(set(c['id'] for c in changes))} row(s) · "
        f"{len(changes)} field change(s) pending"
    )


# =====================================================
# PAGE OPTIONS
# =====================================================

edit_data = st.toggle("Edit mode")

tab1, tab2, tab3 = st.tabs(["Browse Data", "Quick Queries", "Custom Query"])

# =====================================================
# TAB 1 — BROWSE DATA
# =====================================================

with tab1:
    st.subheader("Browse database tables")

    selected_table = st.selectbox("Select table", list(TABLES.keys()))
    is_junction    = not TABLES[selected_table]["editable"]

    limit = st.number_input("Row limit", min_value=1, max_value=10000, value=100)

    # ── Query ─────────────────────────────────────────────────────────────────

    if st.button("Run query"):
        try:
            data = query_data(selected_table, limit)

            if not data:
                st.warning("No data found")
                for k in ["query_results", "original_df", "pending_changes"]:
                    st.session_state[k] = None
            else:
                df = pd.DataFrame(data)
                st.session_state.query_results   = df
                st.session_state.original_df     = df.copy()
                st.session_state.pending_changes = None

        except Exception as e:
            st.error("Query failed")
            st.exception(e)

    # ── Results ───────────────────────────────────────────────────────────────

    if st.session_state.query_results is not None:

        df = st.session_state.query_results.copy()

        # Filters
        st.subheader("Filters")
        col1, col2 = st.columns(2)
        with col1:
            filter_col = st.selectbox("Filter column", [""] + list(df.columns))
        with col2:
            filter_val = st.text_input("Contains value")

        if filter_col and filter_val:
            df = df[
                df[filter_col]
                .astype(str)
                .str.contains(filter_val, case=False, na=False)
            ]

        # Column selector
        selected_columns = st.multiselect(
            "Columns to display",
            list(df.columns),
            default=list(df.columns)
        )
        if selected_columns:
            df = df[selected_columns]

        # Metrics
        m1, m2 = st.columns(2)
        m1.metric("Rows returned",     len(df))
        m2.metric("Columns displayed", len(df.columns))

        # Download
        st.download_button(
            "⬇️ Download results",
            df.to_csv(index=False).encode("utf-8"),
            f"{selected_table}.csv",
            "text/csv"
        )

        # ── Edit mode ─────────────────────────────────────────────────────────

        if edit_data:

            if is_junction:
                st.caption(
                    "Junction table — rows cannot be edited directly. "
                    "Delete and re-add memberships via the Ingest page."
                )
                st.dataframe(df, use_container_width=True)

            else:
                st.subheader("✏️ Edit data")

                edit_method = st.radio(
                    "Edit method",
                    ["Edit inline", "Upload CSV"],
                    horizontal=True
                )

                st.divider()

                # ── Inline editor ─────────────────────────────────────────────

                if edit_method == "Edit inline":

                    # Key is stable for the lifetime of this query result.
                    # Using id() of the dataframe object means the key only
                    # changes when a new query is run and original_df is replaced,
                    # not on every widget rerun — this prevents the editor resetting.
                    editor_key = f"editor_{selected_table}_{id(st.session_state.original_df)}"

                    # Always pass original_df as the base — never feed edited
                    # state back in, as that causes the reset loop.
                    # data_editor manages its own diff state internally via editor_key.
                    st.data_editor(
                        st.session_state.original_df,
                        use_container_width=True,
                        num_rows="fixed",
                        key=editor_key,
                    )

                    if st.button("Preview changes"):
                        changes = compute_changes_from_editor(
                            editor_key,
                            st.session_state.original_df
                        )
                        if not changes:
                            st.info("No changes detected")
                            st.session_state.pending_changes = None
                        else:
                            st.session_state.pending_changes = changes

                # ── CSV upload ────────────────────────────────────────────────

                else:
                    uploaded_file = st.file_uploader("Upload edited CSV", type=["csv"])

                    if uploaded_file:
                        try:
                            uploaded_df = pd.read_csv(uploaded_file)
                            st.write("Preview:")
                            st.dataframe(uploaded_df, use_container_width=True)

                            if st.button("Preview changes"):
                                changes = compute_changes_from_csv(
                                    st.session_state.original_df,
                                    uploaded_df
                                )
                                if not changes:
                                    st.info("No changes detected")
                                    st.session_state.pending_changes = None
                                else:
                                    st.session_state.pending_changes = changes

                        except Exception as e:
                            st.error(f"Failed to read CSV: {e}")

                # ── Pending changes preview ───────────────────────────────────

                if st.session_state.pending_changes:
                    st.subheader("Pending changes")
                    show_pending_changes(st.session_state.pending_changes)

                    col_confirm, col_discard = st.columns([1, 4])

                    with col_confirm:
                        if st.button("✅ Confirm and apply", type="primary"):
                            success, errors = apply_changes(
                                st.session_state.pending_changes,
                                selected_table
                            )
                            if errors:
                                st.error(f"{len(errors)} row(s) failed:")
                                st.json(errors)
                            if success:
                                st.success(f"{success} row(s) updated successfully")

                            # Refresh — fetches latest state and resets editor
                            refreshed = query_data(selected_table, limit)
                            if refreshed:
                                fresh_df = pd.DataFrame(refreshed)
                                st.session_state.query_results   = fresh_df
                                st.session_state.original_df     = fresh_df.copy()
                            st.session_state.pending_changes = None
                            st.rerun()

                    with col_discard:
                        if st.button("✖ Discard changes"):
                            st.session_state.pending_changes = None
                            st.rerun()

        # ── View mode ─────────────────────────────────────────────────────────

        else:
            st.subheader("📄 View data")
            st.dataframe(df, use_container_width=True)

# =====================================================
# TAB 2 — QUICK QUERIES
# =====================================================

with tab2:
    st.subheader("⚡ Quick queries")

    query_name = st.selectbox("Select query", list(QUICK_QUERIES.keys()))

    params = {}
    for param in QUICK_QUERIES[query_name]["params"]:
        params[param] = st.text_input(param.replace("_", " ").title())

    if st.button("Run quick query"):
        try:
            data = run_quick_query(
                QUICK_QUERIES[query_name]["endpoint"],
                **params
            )
            df = pd.DataFrame(data)

            if df.empty:
                st.warning("No results found")
            else:
                st.success(f"{len(df)} rows returned")
                st.dataframe(df, use_container_width=True)

                st.download_button(
                    "⬇️ Download results",
                    df.to_csv(index=False).encode("utf-8"),
                    f"{QUICK_QUERIES[query_name]['endpoint']}.csv",
                    "text/csv"
                )

        except Exception as e:
            st.error("Query failed")
            st.exception(e)

# =====================================================
# TAB 3 — CUSTOM QUERY
# =====================================================

with tab3:
    st.subheader("Custom SQL")
    st.info(
        "Custom SQL queries are coming soon. "
        "Use Browse Data or Quick Queries in the meantime."
    )