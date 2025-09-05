from pydantic import BaseModel, EmailStr

class KeyValueSchema(BaseModel):
    key: str
    value: str

class FetchKeySchema(BaseModel):
    key: str