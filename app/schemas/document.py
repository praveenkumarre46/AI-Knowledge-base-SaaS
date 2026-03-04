from pydantic import BaseModel


class DocumentCreate(BaseModel):
    title: str
    content: str


class DocumentResponse(BaseModel):
    id: int
    title: str
    content: str
    org_id: int

    class Config:
        from_attributes = True