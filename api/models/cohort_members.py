from pydantic import BaseModel, Field, model_validator
from typing import Dict, Any, Optional
from validators.extra_metadata import validate_extra_metadata

class CohortMembersCreate(BaseModel):
    cohort_name: str
    sample_name: str
