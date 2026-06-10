import streamlit as st

st.title("Xavier LIMS")

st.markdown("""
Welcome to the Xavier Laboratory Information Management System (LIMS).

This platform is used to:

* Register projects, samples, experiments, sequencing runs, and files
* Query and review existing metadata
* Update records and relationships
* Track data through the sequencing workflow
* Launch downstream analysis workflows (future functionality)

---

""")

st.header("Getting Started")

st.markdown("""

### 1. Ingest Data

Use the **Ingest** pages to register:

* Projects
* Samples
* Experiments
* Sequencing Runs
* Files

Data can be entered manually or uploaded in bulk using CSV templates.

### 2. Query Data

Use the **Query** pages to search and review existing records.

Relationships between entities are displayed using human-readable names rather than internal IDs.

### 3. Edit Existing Records

Query a table, export records if needed, make modifications, and submit updates back to the system.

Immutable fields:

* id
* created_at
* updated_at

### 4. Review the Data Dictionary

The Data Dictionary contains descriptions of:

* Tables
* Columns
* Allowed values
* Relationships

Consult this page before creating new metadata.
""")

st.header("Data Model")

st.markdown("""
Current hierarchy:

Project
→ Sample
→ Experiment
→ Sequencing Run
→ Files

Relationships are maintained through foreign keys and resolved automatically by the API.
""")

st.info(
"Development Environment: Metadata entered here may be modified or removed during testing."
)

st.sidebar.header("Navigation")

st.sidebar.markdown("""
### Data Ingestion
- Projects
- Samples
- Experiments
- Sequencing Runs
- Files

### Data Query
- Browse Records
- Advanced Query

### Data Management
- Update Records
- Bulk Import
- Bulk Export

### Reference
- Data Dictionary
- Schema Diagram
- API Documentation

### Administration
- System Status
- Audit Logs (future)
""")
