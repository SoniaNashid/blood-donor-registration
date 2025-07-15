class SearchRequest(BaseModel):
    user_id: str
    blood_type: str
    location: str

class ProcessForm(BaseModel):
    request_id: str
    status: str
    comment: str
