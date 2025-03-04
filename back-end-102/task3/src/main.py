import bcrypt
from jose import jwt
from uuid import uuid4
from typing import Union, Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime, timedelta
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

app = FastAPI()

users = [
    {"id": 1, "name": "Adilet", "email": "adilet@example.com", "password": "12341234", "role": "admin"},
    {"id": 2, "name": "Anuar", "email": "anuar@example.com", "password": "12341234", "role": "user"}
]

active_refresh_tokens = {}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

SECRET_KEY = "BaVArIanMotORWorKs3PoInT5LIterTwINTUrBo"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 5
REFRESH_TOKEN_EXPIRE_DAYS = 1

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
    except jwt.JWTError as e:
        print(f"JWT Error: {e}")
        raise HTTPException(status_code=401, detail="Invalid or expired token")

def check_user_role(token_data: dict, required_role: str):
    user_role = token_data.get("role")
    if user_role != required_role:
        raise HTTPException(
            status_code=403,
            detail=f"Access denied: requires {required_role} role"
        )

class UserRequest(BaseModel):
    name: str
    email: EmailStr
    role: str

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
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


@app.get("/protected")
def protected_route(token: str = Depends(oauth2_scheme)):
    user_data = verify_access_token(token)
    return {"message": f"Welcome, your role is {user_data['role']}"}

@app.get("/me")
def get_current_user(token: str = Depends(oauth2_scheme)):
    user_data = verify_access_token(token)
    return {
        "email": user_data["sub"],
        "name": user_data["name"],
        "role": user_data["role"]
    }

@app.get("/admin")
def admin_route(token: str = Depends(oauth2_scheme)):
    user_data = verify_access_token(token)
    check_user_role(user_data, "admin")
    return {"message": "Welcome, Admin! You have full access."}

@app.get("/user-resource")
def user_resource(token: str = Depends(oauth2_scheme)):
    user_data = verify_access_token(token)
    check_user_role(user_data, "user")
    return {"message": f"Welcome, {user_data['name']}! This resource is for users only."}

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
def update_user(user_id: int, user_update: UserUpdate):
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
def delete_user(user_id: int):
    global users
    users = [user for user in users if user["id"] != user_id]
    return {"message": "User deleted successfully!"}