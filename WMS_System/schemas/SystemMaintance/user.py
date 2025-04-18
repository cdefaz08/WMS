from pydantic import BaseModel
from typing import Optional


class UserUpdate(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    role: Optional[str] = None
    full_name: Optional[str] = None
    email_addr: Optional[str] = None
    max_logins: Optional[int] = None
    pall_cap: Optional[int] = None
    comments: Optional[str] = None

class Users(BaseModel):
    username: str
    password: str
    full_name: str
    max_logins: str
    email_addr: str
    pall_cap: float
    comments: str
    role : str