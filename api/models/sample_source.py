from pydantic import BaseModel

class SampleSourceCreate(BaseModel):
    sample_name: str
    pub_id: str
    freezerworks_id: str    # resolves to subject_id via pub_id