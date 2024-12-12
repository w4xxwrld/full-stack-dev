import os
import jwt
import bcrypt
from uuid import uuid4
from dotenv import load_dotenv
from typing import Union, Optional, List
from pydantic import BaseModel, EmailStr
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from fastapi import FastAPI, Depends, HTTPException
from models import UserUpdate, UserResponse, ProjectUpdate, Project, TaskUpdate, Task

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))  
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS")) 

app = FastAPI()

users = [
    {"id": 1, "name": "Adilet", "email": "adilet@example.com", "password": "12341234", "role": "admin"},
    {"id": 2, "name": "Anuar", "email": "anuar@example.com", "password": "12341234", "role": "user"}
]

projects = []

tasks = []

active_refresh_tokens = {}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def create_refresh_token(email: str):
    token_id = str(uuid4())  
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode = {"sub": email, "id": token_id, "exp": expire}
    refresh_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    active_refresh_tokens[token_id] = {"email": email, "expires_at": expire}
    return refresh_token

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(f"Decoded Payload: {payload}")
        return payload
    except jwt.PyJWTError as e:
        print(f"JWT Error: {e}")
        raise HTTPException(status_code=401, detail="Invalid or expired token")

def check_user_role(token_data: dict, required_role: str):
    user_role = token_data.get("role")
    if user_role != required_role:
        raise HTTPException(
            status_code=403,
            detail=f"Access denied: requires {required_role} role"
        )

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/health", status_code=200)
async def health_check():
    return {"status": "healthy"}

@app.post("/auth/register")
def register_user(name: str, email: str, password: str, role: str = "user"):
    if any(u["email"] == email for u in users):
        return {"error": "Email already exists"}
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    new_user = {
        "id": len(users) + 1,
        "name": name,
        "email": email,
        "password": hashed_password,
        "role": role,
    }
    users.append(new_user)
    return {"message": "User registered successfully"}

@app.post("/auth/login")
def login_user(email: str, password: str):
    user = next((u for u in users if u["email"] == email), None)
    if not user or not bcrypt.checkpw(password.encode('utf-8'), user["password"].encode('utf-8')):
        return {"error": "Invalid email or password"}
    
    tokens_to_revoke = [key for key, value in active_refresh_tokens.items() if value["email"] == email]
    for token_id in tokens_to_revoke:
        del active_refresh_tokens[token_id]
    
    access_token = create_access_token({"sub": user["email"], "role": user["role"], "name": user["name"]})
    refresh_token = create_refresh_token(user["email"])
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token
    }

@app.post("/auth/logout")
def logout_user(token: str = Depends(oauth2_scheme)):
    payload = verify_access_token(token)
    email = payload.get("sub")
    
    tokens_to_revoke = [key for key, value in active_refresh_tokens.items() if value["email"] == email]
    for token_id in tokens_to_revoke:
        del active_refresh_tokens[token_id]
    
    return {"message": "Successfully logged out"}

@app.post("/auth/refresh")
def refresh_access_token(refresh_token: str):
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        token_id = payload.get("id")
        email = payload.get("sub")

        if token_id not in active_refresh_tokens:
            raise HTTPException(status_code=401, detail="Refresh token is not active")

        del active_refresh_tokens[token_id]
        new_access_token = create_access_token({"sub": email})
        new_refresh_token = create_refresh_token(email)
        
        return {
            "access_token": new_access_token,
            "refresh_token": new_refresh_token
        }
    
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Refresh token expired")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.get("/users/", response_model=list[UserResponse])
def read_users(token: str = Depends(oauth2_scheme)):
    return users

@app.get("/users/{user_id}", response_model=UserResponse)
def read_user_by_id(user_id: int, token: str = Depends(oauth2_scheme)):
    for user in users:
        if user["id"] == user_id:
            return user
    raise HTTPException(status_code=404, detail="User not found")

@app.put("/users/{user_id}")
def update_user(user_id: int, user_update: UserUpdate, token: str = Depends(oauth2_scheme)):
    for user in users:
        if user["id"] == user_id:
            if user_update.name is not None:
                user["name"] = user_update.name
            if user_update.email is not None:
                user["email"] = user_update.email
            if user_update.role is not None:
                user["role"] = user_update.role
            return {"message": "User updated successfully!", "user": user}
    raise HTTPException(status_code=404, detail="User not found")

@app.delete("/users/{user_id}")
def delete_user(user_id: int, token: str = Depends(oauth2_scheme)):
    global users
    users = [user for user in users if user["id"] != user_id]
    return {"message": "User deleted successfully!"}

@app.post("/projects", response_model=Project)
def create_project(project: Project, token: str = Depends(oauth2_scheme)):
    user_data = verify_access_token(token)
    project_dict = project.dict()
    project_dict["id"] = len(projects) + 1
    project_dict["owner_email"] = user_data["sub"]
    projects.append(project_dict)
    return project_dict

@app.get("/projects", response_model=List[Project])
def get_projects(token: str = Depends(oauth2_scheme)):
    verify_access_token(token)
    return projects

@app.get("/projects/{project_id}", response_model=Project)
def get_project(project_id: int, token: str = Depends(oauth2_scheme)):
    verify_access_token(token)
    for project in projects:
        if project["id"] == project_id:
            return project
    raise HTTPException(status_code=404, detail="Project not found")

@app.put("/projects/{project_id}")
def update_project(project_id: int, project_update: ProjectUpdate, token: str = Depends(oauth2_scheme)):
    user_data = verify_access_token(token)
    for project in projects:
        if project["id"] == project_id:
            if project_update.name is not None:
                project["name"] = project_update.name
            if project_update.description is not None:
                project["description"] = project_update.description
            if project_update.owner_email is not None:
                project["owner_email"] = project_update.owner_email
            return {"message": "Project updated successfully!", "project": project}
    raise HTTPException(status_code=404, detail="Project not found")

@app.delete("/projects/{project_id}")
def delete_project(project_id: int, token: str = Depends(oauth2_scheme)):
    user_data = verify_access_token(token)
    global projects
    for project in projects:
        if project["id"] == project_id and project["owner_email"] == user_data["sub"]:
            projects = [p for p in projects if p["id"] != project_id]
            return {"message": "Project deleted successfully"}
    raise HTTPException(status_code=403, detail="Unauthorized or project not found")

@app.post("/tasks", response_model=Task)
def create_task(task: Task, token: str = Depends(oauth2_scheme)):
    verify_access_token(token)
    task_dict = task.dict()
    task_dict["id"] = len(tasks) + 1
    tasks.append(task_dict)
    return task_dict

@app.get("/tasks", response_model=List[Task])
def get_tasks(token: str = Depends(oauth2_scheme)):
    verify_access_token(token)
    return tasks

@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int, token: str = Depends(oauth2_scheme)):
    verify_access_token(token)
    for task in tasks:
        if task["id"] == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")

@app.put("/tasks/{task_id}")
def update_task(task_id: int, task_update: TaskUpdate, token: str = Depends(oauth2_scheme)):
    for task in tasks:
        if task["id"] == task_id:
            if task_update.title is not None:
                task["title"] = task_update.title
            if task_update.description is not None:
                task["description"] = task_update.description
            if task_update.status is not None:
                task["status"] = task_update.status
            if task_update.project_id is not None:
                task["project_id"] = task_update.project_id
            return {"message": "Task updated successfully!", "task": task}
    raise HTTPException(status_code=404, detail="Task not found")

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, token: str = Depends(oauth2_scheme)):
    verify_access_token(token)
    global tasks
    tasks = [task for task in tasks if task["id"] != task_id]
    return {"message": "Task deleted successfully"}