from fastapi import FastAPI, Depends, HTTPException, Query, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from pydantic import BaseModel
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional, List
from . import models, schemas, crud
from .database import SessionLocal, engine, get_db
from .auth import oauth2_scheme

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from . import models, schemas, crud
from .database import SessionLocal, engine

import os
from .crud import calcular_plan_amortizacion

# Initialize the FastAPI app
models.Base.metadata.create_all(bind=engine)
app = FastAPI()

# CORS middleware configuration
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Secret key to sign the JWT token
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Function to get user from database
def get_user(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

# Function to create access token
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Dependency to get the current user based on the token
def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
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
    except JWTError:
        raise credentials_exception
    user = get_user(db, username=username)
    if user is None:
        raise credentials_exception
    return user

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoint to generate access token
@app.post("/token")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.id}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud.create_user(db=db, user=user)

@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@app.post("/creditos/user_id ", response_model=schemas.Credito)
def create_credito(credito: schemas.CreditoCreate, user_id: int = Query(..., description="User ID"), db: Session = Depends(get_db)):
    return crud.create_credito(db=db, credito=credito, user_id=user_id)

# Define la ruta para obtener créditos filtrados por user_id
@app.get("/creditos/", response_model=List[schemas.Credito])
def read_creditos(user_id: int = Query(None, description="Filtrar créditos por User ID"), skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    if user_id:
        creditos = crud.get_creditos_for_id(db, user_id=user_id, skip=skip, limit=limit)
    else:
        creditos = crud.get_creditos(db, skip=skip, limit=limit)
    return creditos

@app.get("/")
def read_root():
    return {"message": "Bienvenido al Mini Sistema de Créditos"}


# Función para autenticar a un usuario
def authenticate_user(db: Session, username: str, password: str):
    user = crud.get_user_by_username(db, username=username)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user

# Función para verificar la contraseña
def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud.create_user(db=db, user=user)

# Otras rutas y funciones de la API FastAPI



# Endpoint para generar el plan de amortización de un crédito específico
@app.get("/creditos/{user_id}/plan-amortizacion", response_model=List[schemas.PlanAmortizacion])
async def generar_plan_amortizacion(user_id: int, db: Session = Depends(get_db)):
    creditos = crud.get_creditos_for_id(db, user_id=user_id)

    if not creditos:
        raise HTTPException(status_code=404, detail="Crédito no encontrado")

    # plan_amortizacion = crud.calcular_plan_amortizacion(creditos)
    plan_amortizacion = crud.calcular_plan_amortizacion(creditos)




    return []