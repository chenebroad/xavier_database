import json
import streamlit as st
import pandas as pd
from api_client import (
    query_data, run_quick_query, update_row, run_sql_query,
    delete_project, delete_sample, delete_subject, delete_cohort,
    delete_experiment, delete_pool, delete_run, delete_flowcell_library, delete_file,
)

st.header("🔍 Query Data")

# =====================================================
# CONFIG
# =====================================================

TABLES = {
    "projects":           {"editable": True},
    "subjects":           {"editable": True},
    "samples":            {"editable": True},
    "sample_sources":     {"editable": False},  # junction
    "cohorts":            {"editable": True},
    "cohort_members":     {"editable": False},  # junction
    "experiments":        {"editable": True},
    "pools":              {"editable": True},
    "pool_members":       {"editable": False},  # junction
    "sequencing_runs":    {"editable": True},
    "flowcell_libraries": {"editable": False},  # junction-like
    "files":              {"editable": True},
}

# Maps table names to their delete API functions.
# Junction tables are omitted — they have no surrogate id column.
DELETE_FN = {
    "projects":        delete_project,
    "subjects":        delete_subject,
    "samples":         delete_sample,
    "cohorts":         delete_cohort,
    "experiments":     delete_experiment,
    "pools":           delete_pool,
    "sequencing_runs": delete_run,
    "files":           delete_file,
}

QUICK_QUERIES = {
    "All Samples from Project": {
        "endpoint": "samples_by_project",
        "params":   [{"key": "project_name", "fetch_from": ("projects", "project_name")}]
    },
    "All Experiments from Sample": {
        "endpoint": "experiments_by_sample",
        "params":   [{"key": "sample_name", "fetch_from": ("samples", "sample_name")}]
    },
    "All Files from Sample": {
        "endpoint": "files_by_sample",
        "params":   [{"key": "sample_name", "fetch_from": ("samples", "sample_name")}]
    },
    "All Files from Project": {
        "endpoint": "files_by_project",
        "params":   [{"key": "project_name", "fetch_from": ("projects", "project_name")}]
    },
    "All Samples from Cohort": {
        "endpoint": "samples_by_cohort",
        "params":   [{"key": "cohort_name", "fetch_from": ("cohorts", "cohort_name")}]
    },
    "All Subjects from Sample": {
        "endpoint": "subjects_by_sample",
        "params":   [{"key": "sample_name", "fetch_from": ("samples", "sample_name")}]
    },
    "All Experiments from Pool": {
        "endpoint": "experiments_by_pool",
        "params":   [{"key": "pool_name", "fetch_from": ("pools", "pool_name")}]
    },
}

# =====================================================
# SESSION STATE
# =====================================================

for key in ["query_results", "original_df", "pending_changes", "pending_deletes"]:
    if key not in st.session_state:
        st.session_state[key] = None

# =====================================================
# HELPERS
# =====================================================

def normalize_value(v):
    if v is None or v == "":
        return None
    if isinstance(v, dict):
        return json.dumps(v, sort_keys=True)
    if isinstance(v, str):
        stripped = v.strip()
        try:
            parsed = json.loads(stripped.replace("'", '"'))
            return json.dumps(parsed, sort_keys=True)
        except Exception:
            return stripped
    return v


def compute_changes_from_editor(editor_key: str, original_df: pd.DataFrame) -> list[dict]:
    editor_state = st.session_state.get(editor_key)
    if not editor_state:
        return []
    raw_edits = editor_state.get("edited_rows", {})
    changes   = []
    for row_idx_str, field_changes in raw_edits.items():
        row_idx      = int(row_idx_str)
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


@st.cache_data(ttl=60)
def fetch_options(table: str, name_col: str) -> list[str]:
    try:
        data = query_data(table, limit=500)
        return sorted({r[name_col] for r in data if r.get(name_col)})
    except Exception:
        return []


def apply_changes(changes: list[dict], table: str) -> tuple[int, list[dict]]:
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


def apply_deletes(ids: list, table: str) -> tuple[int, list[dict]]:
    delete_fn = DELETE_FN.get(table)
    if not delete_fn:
        return 0, [{"error": f"No delete function registered for '{table}'"}]
    success, errors = 0, []
    for row_id in ids:
        try:
            delete_fn(row_id)
            success += 1
        except Exception as e:
            errors.append({"id": row_id, "error": str(e)})
    return success, errors


def show_pending_changes(changes: list[dict]) -> None:
    change_df = pd.DataFrame(changes)[["row", "field", "from", "to"]]
    st.dataframe(change_df, use_container_width=True, hide_index=True)
    st.caption(
        f"{len(set(c['id'] for c in changes))} row(s) · "
        f"{len(changes)} field change(s) pending"
    )


def filter_metadata(df: pd.DataFrame, key: str, val: str) -> pd.DataFrame:
    def _match(cell):
        if isinstance(cell, dict):
            return str(cell.get(key, "")) == val
        if isinstance(cell, str):
            try:
                return str(json.loads(cell).get(key, "")) == val
            except Exception:
                return False
        return False
    return df[df["extra_metadata"].apply(_match)]


# =====================================================
# PAGE OPTIONS
# =====================================================

edit_data = st.toggle("Edit mode")

tab1, tab2, tab3 = st.tabs(["Browse Data", "Quick Queries", "Custom SQL"])

# =====================================================
# TAB 1 — BROWSE DATA
# =====================================================

with tab1:
    st.subheader("Browse database tables")

    selected_table = st.selectbox("Select table", list(TABLES.keys()))
    is_junction    = not TABLES[selected_table]["editable"]

    limit = st.number_input("Row limit", min_value=1, max_value=10000, value=100)

    if st.button("Run query"):
        try:
            data = query_data(selected_table, limit)
            if not data:
                st.warning("No data found")
                for k in ["query_results", "original_df", "pending_changes", "pending_deletes"]:
                    st.session_state[k] = None
            else:
                df = pd.DataFrame(data)
                st.session_state.query_results   = df
                st.session_state.original_df     = df.copy()
                st.session_state.pending_changes = None
                st.session_state.pending_deletes = None
        except Exception as e:
            st.error("Query failed")
            st.exception(e)

    # ── Results ───────────────────────────────────────────────────────────────

    if st.session_state.query_results is not None:

        df = st.session_state.query_results.copy()

        # ── Filters ───────────────────────────────────────────────────────────

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

        # ── Metadata filter ───────────────────────────────────────────────────

        if "extra_metadata" in df.columns:
            with st.expander("Filter by extra_metadata field"):
                st.caption(
                    "Filters the already-fetched rows. "
                    "For complex JSONB queries across large datasets, use the Custom SQL tab."
                )
                mc1, mc2 = st.columns(2)
                with mc1:
                    meta_key = st.text_input("Metadata key", placeholder="e.g. antibody")
                with mc2:
                    meta_val = st.text_input("Metadata value", placeholder="e.g. H3K27ac")
                if meta_key and meta_val:
                    df = filter_metadata(df, meta_key, meta_val)
                    st.caption(f"Showing rows where extra_metadata['{meta_key}'] = '{meta_val}'")

        # ── Column selector ───────────────────────────────────────────────────

        selected_columns = st.multiselect(
            "Columns to display",
            list(df.columns),
            default=list(df.columns)
        )
        if selected_columns:
            df = df[selected_columns]

        m1, m2 = st.columns(2)
        m1.metric("Rows returned",     len(df))
        m2.metric("Columns displayed", len(df.columns))

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
                    "Junction table — rows cannot be edited or deleted directly. "
                    "Remove and re-add memberships via the Ingest page."
                )
                st.dataframe(df, use_container_width=True)

            else:
                st.subheader("✏️ Edit / Delete")

                edit_method = st.radio(
                    "Action",
                    ["Edit inline", "Upload CSV", "Delete records"],
                    horizontal=True
                )

                st.divider()

                # ── Inline editor ─────────────────────────────────────────────

                if edit_method == "Edit inline":

                    editor_key = f"editor_{selected_table}_{id(st.session_state.original_df)}"

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

                elif edit_method == "Upload CSV":
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

                # ── Delete records ────────────────────────────────────────────

                else:
                    if "id" not in st.session_state.original_df.columns:
                        st.caption("This table has no surrogate id column — deletion is not supported here.")
                    elif selected_table not in DELETE_FN:
                        st.caption("Deletion is not configured for this table.")
                    else:
                        ids = st.session_state.original_df["id"].tolist()

                        to_delete = st.multiselect(
                            "Select record IDs to delete",
                            options=ids,
                        )

                        if to_delete:
                            preview = st.session_state.original_df[
                                st.session_state.original_df["id"].isin(to_delete)
                            ]
                            st.dataframe(preview, use_container_width=True)

                            st.warning(
                                f"**{len(to_delete)} record(s) selected for deletion.** "
                                "This cannot be undone. Child records linked by foreign key "
                                "will also be deleted (cascade).",
                                icon="⚠️"
                            )

                            col_del, col_cancel = st.columns([1, 4])
                            with col_del:
                                if st.button("🗑️ Confirm delete", type="primary"):
                                    success, errors = apply_deletes(to_delete, selected_table)
                                    if errors:
                                        st.error(f"{len(errors)} deletion(s) failed:")
                                        st.json(errors)
                                    if success:
                                        st.success(f"{success} record(s) deleted")
                                    refreshed = query_data(selected_table, limit)
                                    if refreshed:
                                        fresh_df = pd.DataFrame(refreshed)
                                        st.session_state.query_results = fresh_df
                                        st.session_state.original_df   = fresh_df.copy()
                                    else:
                                        st.session_state.query_results = None
                                        st.session_state.original_df   = None
                                    st.session_state.pending_deletes = None
                                    st.rerun()

                # ── Pending edit changes ──────────────────────────────────────

                if st.session_state.pending_changes and edit_method != "Delete records":
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
                            refreshed = query_data(selected_table, limit)
                            if refreshed:
                                fresh_df = pd.DataFrame(refreshed)
                                st.session_state.query_results = fresh_df
                                st.session_state.original_df   = fresh_df.copy()
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
    for param_def in QUICK_QUERIES[query_name]["params"]:
        key        = param_def["key"]
        label      = key.replace("_", " ").title()
        fetch_from = param_def.get("fetch_from")

        options = fetch_options(*fetch_from) if fetch_from else []

        if options:
            selected = st.selectbox(label, [""] + options)
            manual   = st.text_input(
                f"Or type a {label.lower()} manually",
                placeholder="Leave blank to use selection above",
                key=f"manual_{key}"
            )
            params[key] = manual.strip() if manual.strip() else selected
        else:
            params[key] = st.text_input(label, placeholder="Type to search…")
            if fetch_from:
                st.caption("⚠ Could not load options — enter manually")

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
# TAB 3 — CUSTOM SQL
# =====================================================

with tab3:
    st.subheader("Custom SQL")
    st.info(
        "Read-only SELECT queries only. "
        "Use this for JSONB metadata filtering, cross-table joins, "
        "or anything not covered by Quick Queries."
    )

    sql_input = st.text_area(
        "SQL query",
        placeholder="SELECT * FROM experiments WHERE extra_metadata->>'antibody' = 'H3K27ac'",
        height=130,
    )

    if st.button("Run SQL"):
        if not sql_input.strip():
            st.warning("Enter a query first.")
        else:
            try:
                data = run_sql_query(sql_input)
                result_df = pd.DataFrame(data)
                if result_df.empty:
                    st.warning("Query returned no rows.")
                else:
                    st.success(f"{len(result_df)} rows returned")
                    st.dataframe(result_df, use_container_width=True)
                    st.download_button(
                        "⬇️ Download results",
                        result_df.to_csv(index=False).encode("utf-8"),
                        "custom_query.csv",
                        "text/csv",
                    )
            except Exception as e:
                st.error("Query failed")
                st.exception(e)

    with st.expander("JSONB query examples"):
        st.code("""\
-- Filter by a metadata key (string match)
SELECT * FROM experiments
WHERE extra_metadata->>'antibody' = 'H3K27ac';

-- Filter by a metadata key (case-insensitive)
SELECT * FROM samples
WHERE extra_metadata->>'qc_flag' ILIKE '%fail%';

-- Rows that contain a specific metadata key at all
SELECT * FROM files
WHERE extra_metadata ? 'read';

-- Numeric comparison (cast required)
SELECT * FROM files
WHERE (extra_metadata->>'lane')::int = 2;

-- Full-text search across all metadata
SELECT * FROM experiments
WHERE extra_metadata::text ILIKE '%H3K27ac%';

-- Cross-table join with metadata filter
SELECT s.sample_name, e.assay_type, e.extra_metadata
FROM experiments e
JOIN samples s ON e.sample_id = s.id
WHERE e.extra_metadata->>'antibody' = 'H3K27ac'
ORDER BY s.sample_name;
""", language="sql")
