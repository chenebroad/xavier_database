from pydantic import BaseModel, Field, model_validator
from typing import Dict, Any, Optional
from validators.extra_metadata import validate_extra_metadata

class ExperimentCreate(BaseModel):
    sample_name: str
    assay_type: str
    library_prep_date: str
    library_protocol: Optional[str] = None
    library_version: Optional[str] = None
    extra_metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)

    @model_validator(mode="before")
    def check_extra_metadata(cls, values):
        extra = values.get("extra_metadata", {})
        validate_extra_metadata("experiment", extra)
        return values