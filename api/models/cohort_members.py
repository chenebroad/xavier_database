from pydantic import BaseModel, Field, model_validator
from typing import Dict, Any, Optional
from validators.extra_metadata import validate_extra_metadata

class CohortMembersCreate(BaseModel):    
    cohort_id: str
    sample_id: str
    extra_metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)

    @model_validator(mode="before")
    def validate_extra_metadata(cls, values):
        extra_metadata = values.get("extra_metadata", {})
        validate_extra_metadata(extra_metadata)
        return values