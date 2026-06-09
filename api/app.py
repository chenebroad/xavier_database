from fastapi import FastAPI
from endpoints import samples, projects, experiments, sequencingrun, seqexpjunc, files, query, quick_query

app = FastAPI(title="Xavier Database API")

# Include routers
app.include_router(projects.router)
app.include_router(samples.router)
app.include_router(experiments.router)
app.include_router(sequencingrun.router)
app.include_router(seqexpjunc.router)
app.include_router(files.router)
app.include_router(query.router)
app.include_router(quick_query.router)

@app.get("/")
def root():
    return {"message": "LIMS API running"}
