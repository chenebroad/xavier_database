from pydantic import BaseModel, Field, model_validator
from typing import Dict, Any, Optional
from validators.extra_metadata import validate_extra_metadata

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
        extra = values.get("extra_metadata", {})
        validate_extra_metadata("sequencing_run", extra)
        return values
