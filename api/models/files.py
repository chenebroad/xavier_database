from pydantic import BaseModel, Field, model_validator
from typing import Dict, Any, Optional
from validators.extra_metadata import validate_extra_metadata

class FileCreate(BaseModel):
    sample_name: str
    assay_type: str
    library_prep_date: str
    flowcell_id: Optional[str] = None
    lane: Optional [str | int] = None
    gcs_uri: Optional[str] = None
    gcs_bucket: Optional[str] = None
    file_type: Optional[str] = None
    file_format: str
    file_path: Optional[str] = None
    size_bytes: Optional[int] = None
    checksum_md5: Optional[str] = None
    extra_metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)

    @model_validator(mode="before")
    def check_extra_metadata(cls, values):
        extra = values.get("extra_metadata", {})
        validate_extra_metadata("samples", extra)
        return values