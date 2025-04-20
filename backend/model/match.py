from pydantic import BaseModel, HttpUrl

class Metadata(BaseModel):
    source_url: HttpUrl
    source_url_title: str
    text: str
    type: str

class Match(BaseModel):
    id: str
    metadata: Metadata
    score: float
