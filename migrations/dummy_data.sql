INSERT INTO projects (id, project_name, description)
VALUES
('XP00001', 'Liver Cancer Study', 'Study on liver cancer patient samples'),
('XP00002', 'Brain Tissue Study', 'Gene expression in brain samples');

INSERT INTO samples (id, project_id, sample_name, organism, tissue)
VALUES
('XS00001', 'XP00001', 'Liver Patient 001', 'Homo sapiens', 'Liver'),
('XS00002', 'XP00001', 'Liver Patient 002', 'Homo sapiens', 'Liver'),
('XS00003', 'XP00002', 'Brain Donor 001', 'Homo sapiens', 'Brain');

-- IDs auto-generated using sequence, will be XE00001, XE00002, etc.
INSERT INTO experiments (sample_id, assay_type, library_protocol, library_prep_date)
VALUES
('XS00001', 'RNA-seq', 'v2', '2026-02-01'),
('XS00001', 'ATAC-seq', 'v1', '2026-02-02'),
('XS00002', 'RNA-seq', 'v2', '2026-02-03'),
('XS00003', 'RNA-seq', 'v3', '2026-02-05');

-- IDs auto-generated: XR00001, XR00002
INSERT INTO sequencing_runs (flowcell_id, machine, run_date, read_length, sequencing_center)
VALUES
('FC-A123', 'NovaSeq 6000', '2026-02-10', '2x150', 'CoreLab A'),
('FC-B456', 'NovaSeq 6000', '2026-02-12', '2x150', 'CoreLab A');

-- XR00001 sequences XE00001 and XE00003
-- XR00002 sequences XE00002 and XE00001 (resequencing)
INSERT INTO run_experiments (run_id, experiment_id, lane, index_sequence)
VALUES
('XR00001', 'XE00001', 'Lane 1', 'ATCGGA'),
('XR00001', 'XE00003', 'Lane 2', 'GCTTAC'),
('XR00002', 'XE00001', 'Lane 1', 'ATCGGA'),  -- Resequencing XE00001
('XR00002', 'XE00002', 'Lane 2', 'CGTAGC');

INSERT INTO files (run_id, experiment_id, file_type, file_path, checksum)
VALUES
('XR00001', 'XE00001', 'FASTQ', '/data/XS00001/XE00001_R1.fastq.gz', 'abc123'),
('XR00001', 'XE00001', 'FASTQ', '/data/XS00001/XE00001_R2.fastq.gz', 'def456'),
('XR00001', 'XE00003', 'FASTQ', '/data/XS00002/XE00003_R1.fastq.gz', 'ghi789'),
('XR00001', 'XE00003', 'FASTQ', '/data/XS00002/XE00003_R2.fastq.gz', 'jkl012'),
('XR00002', 'XE00001', 'FASTQ', '/data/XS00001/XE00001_R1_reseq.fastq.gz', 'mno345'),
('XR00002', 'XE00001', 'FASTQ', '/data/XS00001/XE00001_R2_reseq.fastq.gz', 'pqr678'),
('XR00002', 'XE00002', 'FASTQ', '/data/XS00001/XE00002_R1.fastq.gz', 'stu901'),
('XR00002', 'XE00002', 'FASTQ', '/data/XS00001/XE00002_R2.fastq.gz', 'vwx234');

INSERT INTO id_concordance (entity_type, internal_id, source_system, external_id)
VALUES
('sample', 'XS00001', 'Terra', 'TERRA_S001'),
('sample', 'XS00002', 'Terra', 'TERRA_S002'),
('experiment', 'XE00001', 'Terra', 'TERRA_XE001'),
('experiment', 'XE00002', 'Terra', 'TERRA_XE002'),
('run', 'XR00001', 'Sequencer', 'FC-A123'),
('run', 'XR00002', 'Sequencer', 'FC-B456');
