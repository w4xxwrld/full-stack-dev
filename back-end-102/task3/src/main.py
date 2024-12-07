from typing import Union
from pydantic import BaseModel, EmailStr
from fastapi import FastAPI, HTTPException

app = FastAPI()

users = [
    {"id": 1, "name": "Adilet", "email": "adilet@example.com", "password": "12341234", "role": "admin"},
    {"id": 2, "name": "Anuar", "email": "anuar@example.com", "password": "12341234", "role": "user"}
]

class UserRequest(BaseModel):
    name: str
    email: EmailStr
    role: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: str

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
    new_user = {
        "id": len(users) + 1,
        "name": name,
        "email": email,
        "password": password,
        "role": role,
    }
    users.append(new_user)
    return {"message": "User registered successfully"}

@app.post("/auth/login")
def login_user(email: str, password: str):
    user = next((u for u in users if u["email"] == email), None)
    if not user or user["password"] != password:
        return {"error": "Invalid email or password"}
    
    return {"message": f"Welcome, {user['name']}"}

@app.get("/users/", response_model=list[UserResponse])
def read_users():
    return users

@app.post("/users", response_model=UserResponse)
def create_user(user: UserRequest):
    global users
    new_user = {"id": len(users) + 1, "name": user.name, "email": user.email, "role": user.role}
    users.append(new_user)
    return new_user

@app.get("/users/{user_id}", response_model=UserResponse)
def read_user_by_id(user_id: int):
    for user in users:
        if user["id"] == user_id:
            return user
    raise HTTPException(status_code=404, detail="User not found")

@app.put("/users/{user_id}")
def update_user(user_id: int, user_name: str, user_email: EmailStr, user_role: str):
    for user in users:
        if user["id"] == user_id:
            user["name"] = user_name
            user["email"] = user_email
            user["role"] = user_role
            return {"message": "User updated successfully!"}
    raise HTTPException(status_code=404, detail="User not found")

@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    global users
    users = [user for user in users if user["id"] != user_id]
    return {"message": "User deleted successfully!"}