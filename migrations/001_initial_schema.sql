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

-- ==============================
-- Projects Table
-- ==============================
CREATE TABLE projects (
    id TEXT PRIMARY KEY DEFAULT ('XP' || LPAD(nextval('project_seq')::TEXT, 5, '0')),
    project_name TEXT NOT NULL UNIQUE,
    description TEXT,
    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now()
);

-- ==============================
-- Samples Table
-- ==============================
CREATE TABLE samples (
    id TEXT PRIMARY KEY DEFAULT ('XS' || LPAD(nextval('sample_seq')::TEXT, 5, '0')),
    project_id TEXT REFERENCES projects(id) ON DELETE CASCADE,
    sample_name TEXT NOT NULL,
    sample_type TEXT NOT NULL,
    subject_id TEXT,
    status TEXT DEFAULT 'active',
	organism TEXT,
    extra_metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now(),
    UNIQUE(project_id, sample_name)
);

-- ==============================
-- Experiments Table
-- ==============================

CREATE TABLE experiments (
    id TEXT PRIMARY KEY 
        DEFAULT ('XE' || LPAD(nextval('experiment_seq')::TEXT, 5, '0')),
        
    sample_id TEXT NOT NULL REFERENCES samples(id) ON DELETE CASCADE,

    assay_type TEXT NOT NULL,
    library_protocol TEXT,
    library_prep_date DATE,
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

-- ==============================
-- Experiment <-> Run Junction Table
-- ==============================

CREATE TABLE run_experiments (
    run_id TEXT REFERENCES sequencing_runs(id) ON DELETE CASCADE,
    experiment_id TEXT REFERENCES experiments(id) ON DELETE CASCADE,

    lane TEXT,
    index_sequence TEXT,
	
    PRIMARY KEY (run_id, experiment_id)
);

-- ==============================
-- Files Table (GCS + Terra Integration)
-- ==============================
CREATE TABLE files (
    id SERIAL PRIMARY KEY,

    run_id TEXT NOT NULL,
    experiment_id TEXT NOT NULL,

    file_type TEXT,      -- FASTQ, BAM, count_matrix, etc.
    file_path TEXT NOT NULL,
    checksum TEXT,
	extra_metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP DEFAULT NOW(),

    FOREIGN KEY (run_id, experiment_id)
        REFERENCES run_experiments(run_id, experiment_id)
        ON DELETE CASCADE
);

-- ==============================
-- Metadata Registry Table
-- Governs allowed keys for JSONB fields
-- ==============================
CREATE TABLE metadata_registry (
    id SERIAL PRIMARY KEY,
    entity_type TEXT NOT NULL,       -- sample, experiment, sequencing_run
    field_name TEXT NOT NULL,        -- tumor_stage, tissue_type, etc.
    data_type TEXT NOT NULL,         -- text, integer, float, boolean, enum
    required BOOLEAN DEFAULT false,
    allowed_values TEXT[],           -- for enums
    description TEXT,
    version INTEGER DEFAULT 1,
    deprecated BOOLEAN DEFAULT false,
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
-- ON samples ((extra_metadata->>'tumor_stage'));

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