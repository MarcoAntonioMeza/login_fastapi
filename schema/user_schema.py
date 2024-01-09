from pydantic import BaseModel
from typing import Optional

class UserSchema(BaseModel):
    id: Optional[int]
    name: str
    username: str
    user_pass: str
