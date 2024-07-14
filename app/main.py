from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

from . import models, schemas, crud
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Configuración de CORS
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependencia para obtener la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/creditos/", response_model=schemas.Credito)
def create_credito(credito: schemas.CreditoCreate, db: Session = Depends(get_db)):
    return crud.create_credito(db=db, credito=credito)

@app.get("/creditos/", response_model=list[schemas.Credito])
def read_creditos(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    creditos = crud.get_creditos(db, skip=skip, limit=limit)
    return creditos

@app.get("/")
def read_root():
    return {"message": "Bienvenido al Mini Sistema de Créditos"}
