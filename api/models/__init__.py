from pydantic import BaseModel, Field, model_validator
from typing import Any, Dict, Optional

from validators.extra_metadata import validate_extra_metadata


class ProjectCreate(BaseModel):
    project_name: str
    description: Optional[str] = None
    extra_metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)

    @model_validator(mode="before")
    def check_extra_metadata(cls, values):
        validate_extra_metadata("projects", values.get("extra_metadata", {}))
        return values


class SubjectCreate(BaseModel):
    pub_id: str
    freezerworks_id: str
    extra_metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)

    @model_validator(mode="before")
    def check_extra_metadata(cls, values):
        validate_extra_metadata("subject", values.get("extra_metadata", {}))
        return values


class SampleCreate(BaseModel):
    project_name: str
    sample_name: str
    sample_type: Optional[str] = "individual"
    organism: Optional[str] = None
    tissue: Optional[str] = None
    extra_metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)

    @model_validator(mode="before")
    def check_extra_metadata(cls, values):
        validate_extra_metadata("samples", values.get("extra_metadata", {}))
        return values


class SampleSourceCreate(BaseModel):
    project_name: str
    sample_name: str
    pub_id: str
    freezerworks_id: str  # resolves to subject_id via pub_id + freezerworks_id


class CohortCreate(BaseModel):
    cohort_name: str
    cohort_type: Optional[str] = None
    description: Optional[str] = None
    extra_metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)

    @model_validator(mode="before")
    def check_extra_metadata(cls, values):
        validate_extra_metadata("cohort", values.get("extra_metadata", {}))
        return values


class CohortMembersCreate(BaseModel):
    cohort_name: str
    project_name: str
    sample_name: str


class ExperimentCreate(BaseModel):
    project_name: str
    sample_name: str
    assay_type: str
    library_prep_date: str
    library_protocol: Optional[str] = None
    library_version: Optional[str] = None
    extra_metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)

    @model_validator(mode="before")
    def check_extra_metadata(cls, values):
        validate_extra_metadata("experiment", values.get("extra_metadata", {}))
        return values


class PoolCreate(BaseModel):
    pool_name: str
    description: Optional[str] = None
    extra_metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)

    @model_validator(mode="before")
    def check_extra_metadata(cls, values):
        validate_extra_metadata("pool", values.get("extra_metadata", {}))
        return values


class PoolMembersCreate(BaseModel):
    pool_name: str
    project_name: str
    sample_name: str
    assay_type: str
    library_prep_date: str  # expects YYYY-MM-DD


class SequencingCreate(BaseModel):
    flowcell_id: str
    machine: Optional[str] = None
    run_date: Optional[str] = None
    read_length: Optional[str] = None
    sequencing_center: Optional[str] = None
    bcl_gcs_uri: Optional[str] = None
    extra_metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)

    @model_validator(mode="before")
    def check_extra_metadata(cls, values):
        validate_extra_metadata("sequencing_run", values.get("extra_metadata", {}))
        return values


class FlowcellLibraryCreate(BaseModel):
    project_name: str
    sample_name: str
    assay_type: str
    library_prep_date: str
    flowcell_id: str
    lane: Optional[str | int] = None
    index_sequence: Optional[str] = None
    extra_metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)

    @model_validator(mode="before")
    def check_extra_metadata(cls, values):
        validate_extra_metadata("experiment", values.get("extra_metadata", {}))
        return values


class FileCreate(BaseModel):
    # Natural keys used to resolve flowcell_library_id
    project_name: str
    sample_name: str
    assay_type: str
    library_prep_date: str
    flowcell_id: str

    # Storage location — at least one required (enforced by DB constraint)
    gcs_uri: Optional[str] = None
    gcs_bucket: Optional[str] = None
    file_path: Optional[str] = None

    file_type: str
    file_format: Optional[str] = None

    # Populated post-demultiplexing for pooled samples
    subject_id: Optional[str] = None

    extra_metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)

    @model_validator(mode="before")
    def check_extra_metadata(cls, values):
        validate_extra_metadata("files", values.get("extra_metadata", {}))
        return values
