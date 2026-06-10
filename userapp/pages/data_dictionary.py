import streamlit as st
import pandas as pd

st.title("📚 Data Dictionary")

st.markdown("""
This page describes the entities, relationships, and fields available within the LIMS system.

### Entity Hierarchy

Projects
→ Samples
→ Experiments
→ Sequencing Runs
→ Files

Additional metadata can be stored in the `extra_metadata` JSON field for each entity.
""")

st.divider()

# =====================================================
# PROJECTS
# =====================================================

with st.expander("📁 Projects", expanded=True):

    st.markdown("""
    Top-level organizational unit.

    A project typically represents a study, grant, collaboration,
    sequencing request, or experimental effort.
    """)

    st.table(
        pd.DataFrame(
            {
                "Field": [
                    "project_name",
                    "description",
                    "extra_metadata"
                ],
                "Required": [
                    "Yes",
                    "No",
                    "No"
                ],
                "Definition": [
                    "Unique project identifier",
                    "Project description",
                    "Additional project metadata"
                ]
            }
        )
    )

# =====================================================
# SAMPLES
# =====================================================

with st.expander("🧬 Samples"):

    st.markdown("""
    Biological samples associated with a project.
    """)

    st.table(
        pd.DataFrame(
            {
                "Field": [
                    "sample_name",
                    "project_name",
                    "subject_id",
                    "status",
                    "organism",
                    "tissue",
                    "extra_metadata"
                ],
                "Required": [
                    "Yes",
                    "Yes",
                    "No",
                    "No",
                    "No",
                    "No",
                    "No"
                ],
                "Definition": [
                    "Unique sample identifier",
                    "Parent project",
                    "Subject or donor identifier",
                    "Sample status",
                    "Species",
                    "Tissue source",
                    "Additional sample metadata"
                ]
            }
        )
    )

# =====================================================
# EXPERIMENTS
# =====================================================

with st.expander("🧪 Experiments"):

    st.markdown("""
    Library preparation or assay performed on a sample.
    """)

    st.table(
        pd.DataFrame(
            {
                "Field": [
                    "sample_name",
                    "assay_type",
                    "library_prep_date",
                    "library_protocol",
                    "library_version",
                    "extra_metadata"
                ],
                "Required": [
                    "Yes",
                    "Yes",
                    "No",
                    "No",
                    "No",
                    "No"
                ],
                "Definition": [
                    "Parent sample",
                    "Assay performed",
                    "Library prep date",
                    "Protocol used",
                    "Protocol version",
                    "Additional experiment metadata"
                ]
            }
        )
    )

# =====================================================
# SEQUENCING RUNS
# =====================================================

with st.expander("🖥️ Sequencing Runs"):

    st.markdown("""
    Represents a sequencing run or flowcell.
    """)

    st.table(
        pd.DataFrame(
            {
                "Field": [
                    "flowcell_id",
                    "machine",
                    "run_date",
                    "read_length",
                    "sequencing_center",
                    "extra_metadata"
                ],
                "Required": [
                    "Yes",
                    "No",
                    "No",
                    "No",
                    "No",
                    "No"
                ],
                "Definition": [
                    "Unique flowcell identifier",
                    "Sequencing instrument",
                    "Run date",
                    "Read length",
                    "Sequencing center",
                    "Additional run metadata"
                ]
            }
        )
    )

# =====================================================
# RUN ↔ EXPERIMENT LINKS
# =====================================================

with st.expander("🔗 Experiment / Run Associations"):

    st.markdown("""
    Junction table connecting experiments to sequencing runs.

    This allows:

    - One experiment to appear in multiple runs
    - One run to contain multiple experiments
    """)

    st.table(
        pd.DataFrame(
            {
                "Field": [
                    "experiment_id",
                    "run_id"
                ],
                "Definition": [
                    "Linked experiment",
                    "Linked sequencing run"
                ]
            }
        )
    )

# =====================================================
# FILES
# =====================================================

with st.expander("📂 Files"):

    st.markdown("""
    Files generated from sequencing or downstream processing.
    """)

    st.table(
        pd.DataFrame(
            {
                "Field": [
                    "gcs_uri",
                    "gcs_bucket",
                    "file_path",
                    "size_bytes",
                    "file_type",
                    "file_format",
                    "checksum_md5",
                    "extra_metadata"
                ],
                "Required": [
                    "Yes",
                    "No",
                    "No",
                    "No",
                    "No",
                    "No",
                    "No",
                    "No"
                ],
                "Definition": [
                    "Cloud Storage location",
                    "Storage bucket",
                    "Internal path",
                    "File size",
                    "File category",
                    "File format",
                    "Checksum",
                    "Additional file metadata"
                ]
            }
        )
    )

st.divider()

st.subheader("📖 Notes")

st.info("""
Relationships are maintained internally using foreign keys.

When ingesting or editing data, users should provide natural keys such as:

- project_name
- sample_name
- flowcell_id

The system automatically resolves these to internal database identifiers.
""")