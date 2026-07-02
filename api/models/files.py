from pydantic import BaseModel, Field, model_validator
from typing import Dict, Any, Optional
from validators.extra_metadata import validate_extra_metadata

class FileCreate(BaseModel):
    # Natural keys used to resolve run_experiment_id
    sample_name: str
    assay_type: str
    library_prep_date: str
    flowcell_id: Optional[str] = None

    # Storage location — at least one required (enforced by DB constraint)
    gcs_uri: Optional[str] = None
    gcs_bucket: Optional[str] = None
    file_path: Optional[str] = None

    file_type: str                        # NOT NULL in schema
    file_format: Optional[str] = None
    size_bytes: Optional[int] = None
    checksum_md5: Optional[str] = None

    # Populated post-demultiplexing for pooled samples
    subject_id: Optional[str] = None

    extra_metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)

    @model_validator(mode="before")
    def check_extra_metadata(cls, values):
        extra = values.get("extra_metadata", {})
        validate_extra_metadata("files", extra)
        return values
