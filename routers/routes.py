from fastapi import APIRouter, Depends, HTTPException, status
from config.database import users_collection
from schemas.schema import list_serial, individual_serial
from bson import ObjectId
from models.user_models import User, UserRequest, UserInDB, UserLogin, Token, TokenData
from passlib.context import CryptContext
from typing import Union, Annotated
from datetime import datetime, timedelta, timezone
import jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from config.database import users_collection

router = APIRouter()

# Secret key for JWT encoding and decoding (Should be securely stored)
SECRET_KEY = ""  # Add your secret key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Token expiration time in minutes

# Password hashing context using bcrypt
pass_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme for handling token-based authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


# Helper function to retrieve user details from the database
def get_user(username: str):
    if users_collection.find_one({"username": username}) == None:
        return None
    else:
        return individual_serial(users_collection.find_one({"username": username}))


# Helper function to hash user passwords
def hash_password(password):
    return pass_context.hash(password)


# Helper function to verify hashed passwords
def verify_password(password, hashed_password):
    return pass_context.verify(password, hashed_password)


# Function to create a JWT access token
def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()

    # Set token expiration time
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)

    # Add expiration and subject (username) to the token
    to_encode.update({"exp": expire, "sub": data.get("username")})

    # Encode and return the JWT token
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
    return encoded_jwt


# User registration endpoint
@router.post("/register")
def register_user(user: UserRequest):
    # Check if username is already taken
    if get_user(user.username):
        raise HTTPException(status_code=400, detail="username already registered")

    # Hash the user's password before storing
    hashed_password = hash_password(user.password)

    # Create a new user instance with hashed password
    new_user = UserInDB(**user.model_dump(), hashed_password=hashed_password)

    # Insert new user into the database
    users_collection.insert_one(dict(new_user))


# User login endpoint - returns access token
@router.post("/login")
def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    # Retrieve user details from the database
    user = get_user(form_data.username)

    # Validate username and password
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Generate access token with expiration
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data=user, expires_delta=access_token_expires)

    return Token(access_token=access_token, token_type="bearer")


# Protected user profile endpoint - requires authentication
@router.get("/profile", response_model=User)
def get_user_profile(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Decode the JWT token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception

    # Retrieve user details from the database
    user = get_user(username=token_data.username)
    if user is None:
        raise credentials_exception

    return user
