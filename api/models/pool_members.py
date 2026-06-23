from pydantic import BaseModel, Field, model_validator
from typing import Dict, Any, Optional
from validators.extra_metadata import validate_extra_metadata

class PoolMembersCreate(BaseModel):
    pool_name: str
    sample_name: str
    assay_type: str
    library_prep_date: str  # expects YYYY-MM-DD