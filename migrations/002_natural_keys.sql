-- ==============================
-- LIMS BASE SCHEMA v1
-- Human-readable IDs (XP, XS, XE)
-- JSONB flexible metadata
-- Metadata registry + audit tables
-- ==============================

-- ------------------------------
-- Enable pgcrypto for sequences
-- ------------------------------
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- ------------------------------
-- Sequences for human-readable IDs
-- ------------------------------
CREATE SEQUENCE project_seq START 1;
CREATE SEQUENCE sample_seq START 1;
CREATE SEQUENCE experiment_seq START 1;
CREATE SEQUENCE run_seq START 1;
CREATE SEQUENCE run_exp_seq START 1;
CREATE SEQUENCE files_seq START 1;

-- ==============================
-- Projects Table
-- ==============================
CREATE TABLE projects (
    id TEXT PRIMARY KEY DEFAULT ('XP' || LPAD(nextval('project_seq')::TEXT, 5, '0')),
    project_name TEXT NOT NULL UNIQUE,
    description TEXT,
	extra_metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now()
);

-- ==============================
-- Samples Table
-- ==============================
CREATE TABLE samples (
    id TEXT PRIMARY KEY 
        DEFAULT ('XS' || LPAD(nextval('sample_seq')::TEXT, 5, '0')),

    project_id TEXT NOT NULL
        REFERENCES projects(id) ON DELETE CASCADE,

    sample_name TEXT NOT NULL,
    subject_id TEXT,
    status TEXT DEFAULT 'active',
    organism TEXT,
    tissue TEXT,

    extra_metadata JSONB DEFAULT '{}'::jsonb,

    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now()

);

-- ==============================
-- Experiments Table
-- ==============================

CREATE TABLE experiments (
    id TEXT PRIMARY KEY
        DEFAULT ('XE' || LPAD(nextval('experiment_seq')::TEXT, 5, '0')),

	sample_id TEXT NOT NULL
    	REFERENCES samples(id) ON DELETE CASCADE,
    assay_type TEXT NOT NULL,
    library_prep_date DATE NOT NULL,

    library_protocol TEXT,
    library_version TEXT,

    extra_metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP DEFAULT NOW()
);

-- ==============================
-- Sequencing Runs
-- ==============================
CREATE TABLE sequencing_runs (
    id TEXT PRIMARY KEY
        DEFAULT ('XR' || LPAD(nextval('run_seq')::TEXT, 5, '0')),
    
    flowcell_id TEXT NOT NULL,
    machine TEXT,
    run_date DATE,
    
    read_length TEXT,
    sequencing_center TEXT,
    extra_metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP DEFAULT NOW()
);

ALTER TABLE sequencing_runs
ADD CONSTRAINT sequencing_runs_flowcell_unique
UNIQUE (flowcell_id);

CREATE INDEX idx_sequencing_runs_flowcell
ON sequencing_runs(flowcell_id);

-- ==============================
-- Experiment <-> Run Junction Table
-- ==============================

CREATE TABLE run_experiments (
	id TEXT PRIMARY KEY
		DEFAULT ('XER' || LPAD(nextval('run_exp_seq')::TEXT, 5, '0')),
	experiment_id TEXT NOT NULL,
    run_id TEXT NOT NULL,
    lane TEXT,
    index_sequence TEXT,
	extra_metadata JSONB DEFAULT '{}'::jsonb,

    UNIQUE (experiment_id, run_id, lane),

    FOREIGN KEY (experiment_id)
        REFERENCES experiments(id)
        ON DELETE CASCADE,

    FOREIGN KEY (run_id)
        REFERENCES sequencing_runs(id)
        ON DELETE CASCADE,

	created_at TIMESTAMP DEFAULT NOW()
);


-- ==============================
-- Files Table (GCS + Terra Integration)
-- ==============================
CREATE TABLE files (
    id TEXT PRIMARY KEY
        DEFAULT ('XF' || LPAD(nextval('files_seq')::TEXT, 5, '0')),

    -- Storage location — at least one must be set (enforced below)
    gcs_uri     TEXT UNIQUE,
    gcs_bucket  TEXT,
    file_path   TEXT,            -- local or network path

    file_type   TEXT NOT NULL,   -- 'fastq', 'vcf', 'counts', 'qc_html', 'qc_json'
    file_format TEXT,            -- 'fastq.gz', 'vcf.gz', 'tsv', 'html'

    size_bytes   BIGINT,
    checksum_md5 TEXT,

    run_experiment_id TEXT REFERENCES run_experiments(id) ON DELETE CASCADE,
    experiment_id     TEXT REFERENCES experiments(id)     ON DELETE CASCADE,

    extra_metadata JSONB DEFAULT '{}'::jsonb,

    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),

    -- Exactly one parent
    CONSTRAINT files_single_parent CHECK (
        (run_experiment_id IS NOT NULL)::int +
        (experiment_id     IS NOT NULL)::int
        = 1
    ),

    -- At least one storage location must be set
    CONSTRAINT files_storage_location CHECK (
        gcs_uri IS NOT NULL OR file_path IS NOT NULL
    )
);

CREATE INDEX idx_files_run_experiment ON files(run_experiment_id);
CREATE INDEX idx_files_experiment     ON files(experiment_id);
CREATE INDEX idx_files_metadata_gin   ON files USING GIN(extra_metadata);

-- ==============================
-- Metadata Registry Table
-- Governs allowed keys for JSONB fields
-- ==============================
CREATE TABLE metadata_registry (
    id SERIAL PRIMARY KEY,
    entity_type TEXT NOT NULL,       -- sample, experiment, sequencing_run
    field_name TEXT NOT NULL,        -- tumor_stage, tissue_type, etc.
    data_type TEXT NOT NULL,         -- text, integer, float, boolean, enum
    allowed_values TEXT[],           -- for enums
    description TEXT,
    version INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT now(),
    UNIQUE(entity_type, field_name, version)
);

-- ==============================
-- Schema Migrations Table (Audit & CI/CD)
-- ==============================
CREATE TABLE schema_migrations (
    id SERIAL PRIMARY KEY,
    migration_name TEXT NOT NULL,
    applied_at TIMESTAMP DEFAULT now()
);

-- ==============================
-- Indexes for Flexible Metadata
-- ==============================

-- GIN index on sample extra_metadata JSONB for general querying
CREATE INDEX idx_samples_metadata_gin
ON samples
USING GIN (extra_metadata);

-- Example expression index for a commonly queried field
-- Uncomment / adjust once field is stabilized
-- CREATE INDEX idx_samples_tumor_stage
-- ON samples ((->>'tumor_stage'));

-- Optional indexes for other tables if needed
CREATE INDEX idx_experiments_metadata_gin
ON experiments
USING GIN (extra_metadata);

CREATE INDEX idx_runs_metadata_gin
ON sequencing_runs
USING GIN (extra_metadata);

-- ID concordance

CREATE TABLE id_concordance (
    id SERIAL PRIMARY KEY,

    entity_type TEXT NOT NULL CHECK (
        entity_type IN ('project', 'sample', 'experiment', 'run')
    ),

    internal_id TEXT NOT NULL,
    source_system TEXT NOT NULL,
    external_id TEXT NOT NULL,

    created_at TIMESTAMP DEFAULT NOW(),

    UNIQUE (entity_type, source_system, external_id)
);

-- Index for fast lookup
CREATE INDEX idx_id_concordance_lookup
ON id_concordance (source_system, external_id);

CREATE INDEX idx_projects_name
ON projects(project_name);

CREATE INDEX idx_samples_project
ON samples(project_id);

CREATE INDEX idx_runs_flowcell
ON sequencing_runs(flowcell_id);