from pydantic import BaseModel, EmailStr
from typing import Optional

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[str] = None

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    password: str
    role: str

class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    owner_email: Optional[EmailStr] = None

class Project(BaseModel):
    id: int
    name: str
    description: str
    owner_email: EmailStr

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    project_id: Optional[int] = None

class Task(BaseModel):
    id: int
    title: str
    description: str
    status: str  # "Pending", "In Progress", "Completed"
    project_id: int