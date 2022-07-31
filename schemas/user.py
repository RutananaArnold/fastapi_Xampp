from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    name:Optional[str]
    email:Optional[str]
    password:Optional[str]
    balance:Optional[int]
    accountNumber:Optional[str]
    
class SendMoney(BaseModel):
    balance: Optional[int]
    accountNumber:Optional[str]    