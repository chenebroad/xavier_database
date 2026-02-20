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
CREATE SEQUENCE sequencing_run_seq START 1;
CREATE SEQUENCE file_seq START 1;

-- ==============================
-- 1️⃣ Projects Table
-- ==============================
CREATE TABLE projects (
    id TEXT PRIMARY KEY DEFAULT ('XP' || LPAD(nextval('project_seq')::TEXT, 5, '0')),
    project_name TEXT NOT NULL UNIQUE,
    description TEXT,
    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now()
);

-- ==============================
-- 2️⃣ Samples Table
-- ==============================
CREATE TABLE samples (
    id TEXT PRIMARY KEY DEFAULT ('XS' || LPAD(nextval('sample_seq')::TEXT, 5, '0')),
    project_id TEXT REFERENCES projects(id) ON DELETE CASCADE,
    sample_name TEXT NOT NULL,
    sample_type TEXT NOT NULL,
    subject_id TEXT,
    status TEXT DEFAULT 'active',
    extra_metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now(),
    UNIQUE(project_id, sample_name)
);

-- ==============================
-- 3️⃣ Experiments Table
-- ==============================
CREATE TABLE experiments (
    id TEXT PRIMARY KEY DEFAULT ('XE' || LPAD(nextval('experiment_seq')::TEXT, 5, '0')),
    project_id TEXT REFERENCES projects(id) ON DELETE CASCADE,
    experiment_name TEXT NOT NULL,
    experiment_type TEXT NOT NULL,
    extra_metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP DEFAULT now(),
    UNIQUE(project_id, experiment_name)
);

-- ==============================
-- 4️⃣ Sample ↔ Experiment Junction Table
-- ==============================
CREATE TABLE sample_experiments (
    sample_id TEXT REFERENCES samples(id) ON DELETE CASCADE,
    experiment_id TEXT REFERENCES experiments(id) ON DELETE CASCADE,
    PRIMARY KEY (sample_id, experiment_id)
);

-- ==============================
-- 5️⃣ Sequencing Runs
-- ==============================
CREATE TABLE sequencing_runs (
    id TEXT PRIMARY KEY DEFAULT ('XR' || LPAD(nextval('sequencing_run_seq')::TEXT, 5, '0')),
    experiment_id TEXT REFERENCES experiments(id) ON DELETE CASCADE,
    platform TEXT,       -- e.g., NovaSeq, NextSeq
    flowcell_id TEXT,
    run_date DATE,
    extra_metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP DEFAULT now()
);

-- ==============================
-- 6️⃣ Files Table (GCS + Terra Integration)
-- ==============================
CREATE TABLE files (
    id TEXT PRIMARY KEY DEFAULT ('XF' || LPAD(nextval('file_seq')::TEXT, 5, '0')),
    sample_id TEXT REFERENCES samples(id) ON DELETE CASCADE,
    sequencing_run_id TEXT REFERENCES sequencing_runs(id) ON DELETE SET NULL,
    file_type TEXT NOT NULL,  -- fastq, bam, count_matrix, etc.
    gcs_uri TEXT NOT NULL,    -- gs://bucket/path/file
    checksum TEXT,
    file_size BIGINT,
    created_at TIMESTAMP DEFAULT now()
);

-- ==============================
-- 7️⃣ Metadata Registry Table
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
-- 8️⃣ Schema Migrations Table (Audit & CI/CD)
-- ==============================
CREATE TABLE schema_migrations (
    id SERIAL PRIMARY KEY,
    migration_name TEXT NOT NULL,
    applied_at TIMESTAMP DEFAULT now()
);

-- ==============================
-- 9️⃣ Indexes for Flexible Metadata
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

CREATE TABLE id_concordance (
    id SERIAL PRIMARY KEY,

    entity_type TEXT NOT NULL,     -- project, sample, experiment, sequencing_run
    internal_id TEXT NOT NULL,     -- XP00001, XS00001, etc.

    external_system TEXT NOT NULL, -- Terra, Biobank, SequencingCenter, ClinicalDB
    external_id TEXT NOT NULL,     -- the alternate ID

    is_primary BOOLEAN DEFAULT false,  -- if this is preferred external ID
    notes TEXT,

    created_at TIMESTAMP DEFAULT now(),

    UNIQUE(entity_type, external_system, external_id),
    UNIQUE(entity_type, internal_id, external_system)
);

-- Index for fast lookup
CREATE INDEX idx_id_concordance_lookup
ON id_concordance (external_system, external_id);