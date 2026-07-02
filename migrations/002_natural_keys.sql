-- ==============================
-- XAVIER LIMS SCHEMA v2
-- Natural human-readable IDs (XP, XS, XE, ...)
-- JSONB flexible metadata
-- ==============================

-- ------------------------------
-- Extensions
-- ------------------------------
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- ------------------------------
-- Sequences for human-readable IDs
-- ------------------------------
CREATE SEQUENCE IF NOT EXISTS project_seq  START 1;
CREATE SEQUENCE IF NOT EXISTS sample_seq   START 1;
CREATE SEQUENCE IF NOT EXISTS subject_seq  START 1;
CREATE SEQUENCE IF NOT EXISTS experiment_seq START 1;
CREATE SEQUENCE IF NOT EXISTS run_seq      START 1;
CREATE SEQUENCE IF NOT EXISTS fl_lib_seq   START 1;
CREATE SEQUENCE IF NOT EXISTS files_seq    START 1;
CREATE SEQUENCE IF NOT EXISTS cohort_seq   START 1;
CREATE SEQUENCE IF NOT EXISTS pool_seq     START 1;

-- ==============================
-- Projects
-- ==============================
CREATE TABLE projects (
    id           TEXT PRIMARY KEY
                     DEFAULT ('XP' || LPAD(nextval('project_seq')::TEXT, 5, '0')),
    project_name TEXT NOT NULL UNIQUE,
    description  TEXT,
    extra_metadata JSONB DEFAULT '{}'::jsonb,
    created_at   TIMESTAMP DEFAULT now(),
    updated_at   TIMESTAMP DEFAULT now()
);

-- ==============================
-- Subjects
-- (Independent of samples — linked via sample_sources)
-- ==============================
CREATE TABLE subjects (
    id               TEXT PRIMARY KEY
                         DEFAULT ('XSU' || LPAD(nextval('subject_seq')::TEXT, 5, '0')),
    pub_id           TEXT NOT NULL,
    freezerworks_id  TEXT NOT NULL,
    extra_metadata   JSONB DEFAULT '{}'::jsonb,
    added_at         TIMESTAMP DEFAULT now(),
    UNIQUE (pub_id, freezerworks_id)
);

-- ==============================
-- Samples
-- ==============================
CREATE TABLE samples (
    id           TEXT PRIMARY KEY
                     DEFAULT ('XS' || LPAD(nextval('sample_seq')::TEXT, 5, '0')),
    project_id   TEXT NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    sample_name  TEXT NOT NULL,
    sample_type  TEXT DEFAULT 'individual',   -- 'individual' | 'pooled'
    organism     TEXT,
    tissue       TEXT,
    extra_metadata JSONB DEFAULT '{}'::jsonb,
    created_at   TIMESTAMP DEFAULT now(),
    updated_at   TIMESTAMP DEFAULT now(),
    UNIQUE (project_id, sample_name)
);

-- ==============================
-- Sample Sources
-- Junction: which subjects contributed to which sample
-- No surrogate ID — composite PK only
-- ==============================
CREATE TABLE sample_sources (
    sample_id  TEXT NOT NULL REFERENCES samples(id)  ON DELETE CASCADE,
    subject_id TEXT NOT NULL REFERENCES subjects(id) ON DELETE CASCADE,
    added_at   TIMESTAMP DEFAULT now(),
    PRIMARY KEY (sample_id, subject_id)
);

-- ==============================
-- Cohorts
-- ==============================
CREATE TABLE cohorts (
    id           TEXT PRIMARY KEY
                     DEFAULT ('XC' || LPAD(nextval('cohort_seq')::TEXT, 5, '0')),
    cohort_name  TEXT NOT NULL UNIQUE,
    cohort_type  TEXT,   -- 'biological' | 'technical' | 'analysis'
    description  TEXT,
    extra_metadata JSONB DEFAULT '{}'::jsonb,
    created_at   TIMESTAMP DEFAULT now(),
    updated_at   TIMESTAMP DEFAULT now()
);

-- ==============================
-- Cohort Members
-- Junction: which samples belong to which cohort
-- No surrogate ID — composite PK only
-- ==============================
CREATE TABLE cohort_members (
    cohort_id  TEXT NOT NULL REFERENCES cohorts(id)  ON DELETE CASCADE,
    sample_id  TEXT NOT NULL REFERENCES samples(id)  ON DELETE CASCADE,
    added_at   TIMESTAMP DEFAULT now(),
    PRIMARY KEY (cohort_id, sample_id)
);

-- ==============================
-- Experiments
-- ==============================
CREATE TABLE experiments (
    id                TEXT PRIMARY KEY
                          DEFAULT ('XE' || LPAD(nextval('experiment_seq')::TEXT, 5, '0')),
    sample_id         TEXT NOT NULL REFERENCES samples(id) ON DELETE CASCADE,
    assay_type        TEXT NOT NULL,
    library_protocol  TEXT,
    library_version   TEXT,
    library_prep_date DATE,
    extra_metadata    JSONB DEFAULT '{}'::jsonb,
    created_at        TIMESTAMP DEFAULT now(),
    updated_at        TIMESTAMP DEFAULT now(),
    UNIQUE (sample_id, assay_type, library_prep_date)
);

-- ==============================
-- Pools
-- ==============================
CREATE TABLE pools (
    id           TEXT PRIMARY KEY
                     DEFAULT ('XPO' || LPAD(nextval('pool_seq')::TEXT, 5, '0')),
    pool_name    TEXT NOT NULL UNIQUE,
    description  TEXT,
    extra_metadata JSONB DEFAULT '{}'::jsonb,
    created_at   TIMESTAMP DEFAULT now(),
    updated_at   TIMESTAMP DEFAULT now()
);

-- ==============================
-- Pool Members
-- Junction: which experiments belong to which pool
-- No surrogate ID — composite PK only
-- ==============================
CREATE TABLE pool_members (
    pool_id       TEXT NOT NULL REFERENCES pools(id)       ON DELETE CASCADE,
    experiment_id TEXT NOT NULL REFERENCES experiments(id) ON DELETE CASCADE,
    added_at      TIMESTAMP DEFAULT now(),
    PRIMARY KEY (pool_id, experiment_id)
);

-- ==============================
-- Sequencing Runs
-- ==============================
CREATE TABLE sequencing_runs (
    id                TEXT PRIMARY KEY
                          DEFAULT ('XR' || LPAD(nextval('run_seq')::TEXT, 5, '0')),
    flowcell_id       TEXT NOT NULL UNIQUE,
    machine           TEXT,
    run_date          DATE,
    read_length       TEXT,
    sequencing_center TEXT,
    bcl_gcs_uri       TEXT,
    extra_metadata    JSONB DEFAULT '{}'::jsonb,
    created_at        TIMESTAMP DEFAULT now(),
    updated_at        TIMESTAMP DEFAULT now()
);

-- ==============================
-- Flowcell Libraries
-- Pre-sequencing manifest: which library is on which flowcell, lane, and index.
-- Parent record for all raw FASTQ files produced by demultiplexing.
-- ==============================
CREATE TABLE flowcell_libraries (
    id             TEXT PRIMARY KEY
                       DEFAULT ('XER' || LPAD(nextval('fl_lib_seq')::TEXT, 5, '0')),
    experiment_id  TEXT NOT NULL REFERENCES experiments(id)     ON DELETE CASCADE,
    run_id         TEXT NOT NULL REFERENCES sequencing_runs(id) ON DELETE CASCADE,
    lane           TEXT,
    index_sequence TEXT,
    extra_metadata JSONB DEFAULT '{}'::jsonb,
    created_at     TIMESTAMP DEFAULT now(),
    updated_at     TIMESTAMP DEFAULT now(),
    UNIQUE (experiment_id, run_id, lane)
);

-- ==============================
-- Files
-- Raw sequencing output files (FASTQs) produced by demultiplexing.
-- Each file belongs to exactly one flowcell_library record.
-- ==============================
CREATE TABLE files (
    id                   TEXT PRIMARY KEY
                             DEFAULT ('XF' || LPAD(nextval('files_seq')::TEXT, 5, '0')),

    flowcell_library_id  TEXT NOT NULL REFERENCES flowcell_libraries(id) ON DELETE CASCADE,

    -- Populated post-demultiplexing for pooled samples
    subject_id           TEXT REFERENCES subjects(id),

    -- Storage location — at least one must be set (enforced below)
    gcs_uri              TEXT UNIQUE,
    gcs_bucket           TEXT,
    file_path            TEXT,

    file_type            TEXT NOT NULL,   -- 'fastq', 'bam', etc.
    file_format          TEXT,            -- 'fastq.gz', 'bam', etc.

    extra_metadata       JSONB DEFAULT '{}'::jsonb,
    created_at           TIMESTAMP DEFAULT now(),
    updated_at           TIMESTAMP DEFAULT now(),

    CONSTRAINT files_storage_location CHECK (
        gcs_uri IS NOT NULL OR file_path IS NOT NULL
    )
);

-- ==============================
-- Indexes
-- ==============================
CREATE INDEX idx_samples_project      ON samples(project_id);
CREATE INDEX idx_samples_metadata_gin ON samples  USING GIN (extra_metadata);
CREATE INDEX idx_experiments_metadata ON experiments USING GIN (extra_metadata);
CREATE INDEX idx_runs_flowcell        ON sequencing_runs(flowcell_id);
CREATE INDEX idx_runs_metadata_gin    ON sequencing_runs USING GIN (extra_metadata);
CREATE INDEX idx_files_flowcell_library ON files(flowcell_library_id);
CREATE INDEX idx_files_subject          ON files(subject_id);
CREATE INDEX idx_files_metadata_gin     ON files USING GIN (extra_metadata);
CREATE INDEX idx_projects_name        ON projects(project_name);

-- ==============================
-- Schema Migrations Audit Table
-- ==============================
CREATE TABLE IF NOT EXISTS schema_migrations (
    id             SERIAL PRIMARY KEY,
    migration_name TEXT NOT NULL,
    applied_at     TIMESTAMP DEFAULT now()
);

INSERT INTO schema_migrations (migration_name) VALUES ('002_natural_keys');
