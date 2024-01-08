from pydantic import BaseModel
from typing import Optional

class UserSchema(BaseModel):
    #id: Optional[str] = None
    name: str
    username: str
    user_pass: str
