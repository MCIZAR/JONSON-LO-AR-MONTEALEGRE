from dataclasses import dataclass
from typing import Optional

@dataclass
class User:
    id: Optional[int]
    username: str
    password: str
    role: str

@dataclass
class Supplier:
    id: Optional[int]
    name: str
    contact: Optional[str] = None
    address: Optional[str] = None

@dataclass
class Part:
    id: Optional[int]
    code: str
    name: str
    description: Optional[str]
    price: float
    quantity: int
    supplier_id: Optional[int]
