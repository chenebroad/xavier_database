from pydantic import BaseModel, Field, model_validator
from typing import Dict, Any, Optional
from ..validators.extra_metadata import validate_extra_metadata

class SequencingCreate(BaseModel):
    flowcell_id: str
    machine: str
    run_date: str
    read_length: str | int
    sequencing_center: str
    extra_metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)

    @model_validator(mode="before")
    def check_extra_metadata(cls, values):
        extra = values.get("extra_metadata", {})
        validate_extra_metadata("experiment", extra)
        return values