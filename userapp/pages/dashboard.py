import streamlit as st
import pandas as pd
import requests
from pathlib import Path

API_BASE = "https://xavier-db-dev-134042435125.us-central1.run.app"


def fetch(endpoint: str):
    try:
        r = requests.get(f"{API_BASE}{endpoint}")
        r.raise_for_status()
        return r.json()
    except Exception as e:
        st.error(f"API error: {e}")
        return []


def dot(filled: bool) -> str:
    return "●" if filled else "○"


def completeness_score(row: dict) -> int:
    return sum([
        bool(row.get("has_subjects")),
        bool(row.get("has_experiment")),
        bool(row.get("has_run")),
    ])


# ── Page config ───────────────────────────────────────────────────────────────

st.set_page_config(page_title="Xavier LIMS — Dashboard", layout="wide")
st.title("Project dashboard")
st.caption("Lineage completeness across all projects.")

# ── Project summary cards ─────────────────────────────────────────────────────

projects = fetch("/dashboard/projects")

if not projects:
    st.info("No projects found. Ingest a project to get started.")
    st.stop()

st.subheader("All projects")

summary_df = pd.DataFrame(projects)

# Metric cards — one per project, up to 4 per row
cols_per_row = 4
rows = [
    projects[i:i + cols_per_row]
    for i in range(0, len(projects), cols_per_row)
]

for row in rows:
    cols = st.columns(cols_per_row)
    for col, project in zip(cols, row):
        score = sum([
            project["sample_count"] > 0,
            project["experiment_count"] > 0,
            project["run_count"] > 0,
            project["file_count"] > 0,
        ])
        status_color = (
            "🟢" if score == 4 else
            "🟡" if score >= 2 else
            "🔴"
        )
        with col:
            st.markdown(f"**{status_color} {project['project_name']}**")
            st.caption(project.get("description") or "No description")
            m1, m2 = st.columns(2)
            m1.metric("Samples",     project["sample_count"])
            m2.metric("Subjects",    project["subject_count"])
            m3, m4 = st.columns(2)
            m3.metric("Experiments", project["experiment_count"])
            m4.metric("Files",       project["file_count"])
            if project["pooled_sample_count"] > 0:
                st.caption(
                    f"{project['pooled_sample_count']} pooled · "
                    f"{project['individual_sample_count']} individual"
                )
            st.divider()

# ── Project drill-down ────────────────────────────────────────────────────────

st.subheader("Sample-level detail")

project_names = [p["project_name"] for p in projects]
selected = st.selectbox("Select project", project_names)

if selected:
    detail     = fetch(f"/dashboard/projects/{selected}")
    cohorts    = fetch(f"/dashboard/projects/{selected}/cohorts")

    if not detail:
        st.info("No samples found for this project.")
        st.stop()

    df = pd.DataFrame(detail)

    # Compute completeness score
    df["completeness"] = df.apply(completeness_score, axis=1)

    # Dot columns
    df["subjects"]    = df["has_subjects"].apply(dot)
    df["experiment"]  = df["has_experiment"].apply(dot)
    df["run"]         = df["has_run"].apply(dot)
    df["files"]       = df["has_files"].apply(dot)

    # Assay types as readable string
    df["assays"] = df["assay_types"].apply(
        lambda x: ", ".join(x) if x else "—"
    )

    display_df = df[[
        "sample_name", "sample_type", "organism", "tissue",
        "assays", "subject_count", "experiment_count",
        "run_count", "file_count",
        "subjects", "experiment", "run", "files",
        "completeness"
    ]].rename(columns={
        "sample_name":      "Sample",
        "sample_type":      "Type",
        "organism":         "Organism",
        "tissue":           "Tissue",
        "assays":           "Assays",
        "subject_count":    "# Subjects",
        "experiment_count": "# Experiments",
        "run_count":        "# Runs",
        "file_count":       "# Files",
        "subjects":         "Subjects ●",
        "experiment":       "Experiment ●",
        "run":              "Run ●",
        "files":            "Files ●",
        "completeness":     "Completeness",
    })

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Completeness": st.column_config.ProgressColumn(
                "Completeness",
                min_value=0,
                max_value=3,
                format="%d / 3",
            ),
            "Type": st.column_config.TextColumn("Type"),
        }
    )

    # Summary line below table
    complete   = (df["completeness"] == 3).sum()
    incomplete = (df["completeness"] < 3).sum()
    st.caption(
        f"{complete} fully complete · "
        f"{incomplete} incomplete · "
        f"{len(df)} total samples"
    )

    # ── Cohort membership ─────────────────────────────────────────────────────
    if cohorts:
        st.subheader("Cohorts in this project")
        cohort_df = pd.DataFrame(cohorts).rename(columns={
            "cohort_name":  "Cohort",
            "cohort_type":  "Type",
            "member_count": "Members",
        })
        st.dataframe(cohort_df, use_container_width=True, hide_index=True)
    else:
        st.caption("No cohorts linked to samples in this project.")