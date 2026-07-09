-- Migration 003: enforce project-scoped uniqueness for sample names
--
-- Previously sample_name was assumed globally unique (no constraint existed).
-- This migration adds the composite constraint so that the same name can exist
-- in different projects, but not twice within the same project.
--
-- Run BEFORE deploying the API changes from this same commit.
-- Safe to run against a populated database — will fail if duplicate
-- (project_id, sample_name) pairs already exist. Resolve those first.

ALTER TABLE samples
    ADD CONSTRAINT samples_name_project_unique UNIQUE (project_id, sample_name);
