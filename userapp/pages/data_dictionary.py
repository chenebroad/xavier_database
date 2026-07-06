import streamlit as st
import pandas as pd

st.title("📚 Data Dictionary")

st.markdown("""
This page describes every entity, relationship, and ingest field in the LIMS system.

### Entity Hierarchy

```
PROJECTS
  └─ SAMPLES ◄── SAMPLE_SOURCES ──► SUBJECTS
       ├─ COHORT_MEMBERS ──► COHORTS
       └─ EXPERIMENTS
            ├─ POOL_MEMBERS ──► POOLS
            └─ FLOWCELL_LIBRARIES ──► SEQUENCING_RUNS
                 └─ FILES
```

**Lineage** (where did this come from?): Projects → Samples → Experiments → Sequencing Runs → Files

**Grouping** (what belongs together?): Cohorts ↔ Samples, Pools ↔ Experiments

All entities support an `extra_metadata` JSON field for extensibility.
Junction tables (sample_sources, cohort_members, pool_members) do not have `extra_metadata`.

When ingesting data, provide natural keys such as `project_name`, `sample_name`, or `flowcell_id`.
The system resolves these to internal IDs automatically.
""")

st.divider()

# =====================================================
# PROJECTS
# =====================================================

with st.expander("📁 Projects", expanded=True):
    st.markdown("Top-level organizational unit. Typically represents a study, grant, or sequencing request.")
    st.table(pd.DataFrame({
        "Field":      ["project_name", "description", "extra_metadata"],
        "Required":   ["Yes", "No", "No"],
        "Definition": [
            "Unique project name",
            "Free-text description",
            "Additional metadata (JSON)"
        ]
    }))

# =====================================================
# SUBJECTS
# =====================================================

with st.expander("👤 Subjects"):
    st.markdown("""
    A donor or subject contributing biological material.
    Subjects are linked to samples via **sample_sources**, not directly on the sample record.
    """)
    st.table(pd.DataFrame({
        "Field":      ["pub_id", "freezerworks_id", "extra_metadata"],
        "Required":   ["Yes", "Yes", "No"],
        "Definition": [
            "Public identifier (e.g. patient ID)",
            "FreezerWorks biobank identifier",
            "Additional metadata (JSON)"
        ]
    }))

# =====================================================
# SAMPLES
# =====================================================

with st.expander("🧬 Samples"):
    st.markdown("""
    Biological samples associated with a project.
    Subject linkage is managed via **sample_sources** — there is no `subject_id` on the sample itself.
    """)
    st.table(pd.DataFrame({
        "Field":      ["sample_name", "project_name", "organism", "tissue", "sample_type", "extra_metadata"],
        "Required":   ["Yes", "Yes", "No", "No", "No", "No"],
        "Definition": [
            "Unique sample identifier",
            "Parent project (resolved to project_id)",
            "Species (e.g. Homo sapiens)",
            "Tissue of origin",
            "'individual' or 'pooled' (default: individual)",
            "Additional metadata (JSON)"
        ]
    }))

# =====================================================
# SAMPLE SOURCES (junction)
# =====================================================

with st.expander("🔗 Sample Sources (junction)"):
    st.markdown("""
    Links samples to their contributing subjects.
    Individual samples have one row; pooled samples have one row per contributing subject.
    Junction table — no `extra_metadata`, no PATCH. Use DELETE + re-insert to update membership.
    """)
    st.table(pd.DataFrame({
        "Field":      ["sample_name", "pub_id", "freezerworks_id"],
        "Required":   ["Yes", "Yes", "Yes"],
        "Definition": [
            "Sample to link (resolved to sample_id)",
            "Subject public ID (resolved to subject_id)",
            "Subject FreezerWorks ID (used with pub_id to identify subject)"
        ]
    }))

# =====================================================
# COHORTS
# =====================================================

with st.expander("👥 Cohorts"):
    st.markdown("Named groupings of samples — biological, technical, or analysis-defined.")
    st.table(pd.DataFrame({
        "Field":      ["cohort_name", "cohort_type", "description", "extra_metadata"],
        "Required":   ["Yes", "No", "No", "No"],
        "Definition": [
            "Unique cohort name",
            "'biological', 'technical', or 'analysis'",
            "Free-text description",
            "Additional metadata (JSON)"
        ]
    }))

# =====================================================
# COHORT MEMBERS (junction)
# =====================================================

with st.expander("🔗 Cohort Members (junction)"):
    st.markdown("""
    Links samples to cohorts.
    Junction table — no `extra_metadata`, no PATCH. Use DELETE + re-insert to update membership.
    """)
    st.table(pd.DataFrame({
        "Field":      ["cohort_name", "sample_name"],
        "Required":   ["Yes", "Yes"],
        "Definition": [
            "Target cohort (resolved to cohort_id)",
            "Sample to add (resolved to sample_id)"
        ]
    }))

# =====================================================
# EXPERIMENTS
# =====================================================

with st.expander("🧪 Experiments"):
    st.markdown("Library preparation or assay performed on a sample.")
    st.table(pd.DataFrame({
        "Field":      ["sample_name", "assay_type", "library_prep_date", "library_protocol", "library_version", "extra_metadata"],
        "Required":   ["Yes", "Yes", "Yes", "No", "No", "No"],
        "Definition": [
            "Parent sample (resolved to sample_id)",
            "Assay type (e.g. RNA-Seq, ATAC-Seq)",
            "Date library was prepared (YYYY-MM-DD)",
            "Protocol used (e.g. 10x Chromium v3)",
            "Protocol version",
            "Additional metadata (JSON)"
        ]
    }))

# =====================================================
# POOLS
# =====================================================

with st.expander("🧪 Pools"):
    st.markdown("Named groupings of experiments that were physically pooled before sequencing.")
    st.table(pd.DataFrame({
        "Field":      ["pool_name", "description", "extra_metadata"],
        "Required":   ["Yes", "No", "No"],
        "Definition": [
            "Unique pool name",
            "Free-text description",
            "Additional metadata (JSON)"
        ]
    }))

# =====================================================
# POOL MEMBERS (junction)
# =====================================================

with st.expander("🔗 Pool Members (junction)"):
    st.markdown("""
    Links experiments to a pool.
    Junction table — no `extra_metadata`, no PATCH. Use DELETE + re-insert to update membership.
    """)
    st.table(pd.DataFrame({
        "Field":      ["pool_name", "sample_name", "assay_type", "library_prep_date"],
        "Required":   ["Yes", "Yes", "Yes", "Yes"],
        "Definition": [
            "Target pool (resolved to pool_id)",
            "Sample name — used together with assay_type and library_prep_date to identify the experiment",
            "Assay type of the experiment",
            "Library prep date of the experiment"
        ]
    }))

# =====================================================
# SEQUENCING RUNS
# =====================================================

with st.expander("🖥️ Sequencing Runs"):
    st.markdown("""
    Represents a physical sequencing run on a flowcell.
    `bcl_gcs_uri` can be used to store the GCS path to the raw BCL output for the run.
    """)
    st.table(pd.DataFrame({
        "Field":      ["flowcell_id", "machine", "run_date", "read_length", "sequencing_center", "bcl_gcs_uri", "extra_metadata"],
        "Required":   ["Yes", "No", "No", "No", "No", "No", "No"],
        "Definition": [
            "Unique flowcell identifier (e.g. HXXXXDRXY)",
            "Sequencing instrument (e.g. NovaSeq 6000)",
            "Date the run completed (YYYY-MM-DD)",
            "Read length (e.g. 150)",
            "Sequencing center or core facility",
            "GCS URI to the raw BCL output directory",
            "Additional metadata (JSON)"
        ]
    }))

# =====================================================
# FLOWCELL LIBRARIES
# =====================================================

with st.expander("🔗 Flowcell Libraries"):
    st.markdown("""
    Pre-registers lane and index assignments for each experiment on a sequencing run.
    Created before file delivery to record the sequencing manifest.
    Links experiments to sequencing runs; files attach here once delivered.
    """)
    st.table(pd.DataFrame({
        "Field":      ["sample_name", "assay_type", "library_prep_date", "flowcell_id", "lane", "index_sequence", "extra_metadata"],
        "Required":   ["Yes", "Yes", "Yes", "Yes", "Yes", "Yes", "No"],
        "Definition": [
            "Sample name — identifies the experiment together with assay_type and library_prep_date",
            "Assay type of the experiment",
            "Library prep date of the experiment",
            "Flowcell ID of the sequencing run (resolved to run_id)",
            "Lane number on the flowcell",
            "Index (barcode) sequence",
            "Additional metadata (JSON)"
        ]
    }))

# =====================================================
# FILES
# =====================================================

with st.expander("📂 Files"):
    st.markdown("""
    Files generated from sequencing or downstream processing.
    Each file is linked to a flowcell library entry (identified by sample_name + assay_type + library_prep_date + flowcell_id).
    Either `gcs_uri` or `file_path` must be provided.
    For post-demultiplexing files from pooled samples, `subject_id` can be populated to attribute the file to a specific subject.
    """)
    st.table(pd.DataFrame({
        "Field":      ["sample_name", "assay_type", "library_prep_date", "flowcell_id", "file_type", "gcs_uri", "gcs_bucket", "file_path", "file_format", "subject_id", "extra_metadata"],
        "Required":   ["Yes", "Yes", "Yes", "Yes", "Yes", "No*", "No", "No*", "No", "No", "No"],
        "Definition": [
            "Identifies the parent flowcell library",
            "Identifies the parent flowcell library",
            "Identifies the parent flowcell library",
            "Identifies the parent flowcell library",
            "File category (e.g. fastq, bam, vcf, counts)",
            "GCS URI to the file (* required if file_path not set)",
            "GCS bucket name",
            "Internal or cluster file path (* required if gcs_uri not set)",
            "File format/extension (e.g. fastq.gz, bam, tsv)",
            "Subject ID — for demultiplexed files from pooled samples",
            "Additional metadata (JSON)"
        ]
    }))

st.divider()

st.subheader("📖 Notes")

st.info("""
**Natural key resolution:** all ingest forms accept human-readable names
(`project_name`, `sample_name`, `flowcell_id`, etc.).
Internal database IDs are never required in ingest forms.

**Junction tables** (sample_sources, cohort_members, pool_members):
- No `extra_metadata` field
- Cannot be edited via PATCH — delete and re-add to update membership

**Pooled samples:** a sample with `sample_type = 'pooled'` has multiple rows in
`sample_sources`, one per contributing subject. Demultiplexed outputs are
registered as files with `subject_id` set — the pooled sample is never split.
""")
