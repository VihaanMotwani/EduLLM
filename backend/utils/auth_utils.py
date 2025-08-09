import os
from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

# --- Local Imports ---
import backend.utils.db_utils as db_utils
from backend.models.pydantic_models import User

# --- Configuration ---
# You should generate a real secret key, e.g., using: openssl rand -hex 32
SECRET_KEY = os.getenv("SECRET_KEY", "your-fallback-secret-key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password Hashing setup
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 Scheme for token-based security
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# --- Pydantic Models ---
class TokenData(BaseModel):
    username: Optional[str] = None

# --- Core Functions ---

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies a plain password against a hashed one."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hashes a plain password."""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Creates a new JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """
    Decodes JWT token to get the current user. This is a FastAPI dependency.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    
    user_data = db_utils.get_user(username=token_data.username)
    if user_data is None:
        raise credentials_exception
        
    return User(**user_data)