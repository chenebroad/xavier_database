from fastapi import FastAPI
from endpoints import (samples, projects, experiments,
cohorts, cohort_members, pools, pool_members,
subjects, sample_sources, sequencing_runs,
flowcell_libraries, files, query, quick_query, dashboard, sql,
metadata_registry)

app = FastAPI(title="Xavier Database API")

# Include routers
# MAIN ROUTERS for INGEST
app.include_router(projects.router)
app.include_router(samples.router)
app.include_router(subjects.router)
app.include_router(sample_sources.router)
app.include_router(cohorts.router)
app.include_router(cohort_members.router)
app.include_router(experiments.router)
app.include_router(pools.router)
app.include_router(pool_members.router)
app.include_router(sequencing_runs.router)
app.include_router(flowcell_libraries.router)
app.include_router(files.router)

# SUPPLEMENTARY ROUTERS for QUERY
app.include_router(query.router)
app.include_router(quick_query.router)
app.include_router(dashboard.router)
app.include_router(sql.router)
app.include_router(metadata_registry.router)

@app.get("/")
def root():
    return {"message": "LIMS API running"}
