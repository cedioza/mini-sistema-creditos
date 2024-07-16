import hashlib
from fastapi import HTTPException
from sqlalchemy.orm import Session
from . import models, schemas
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
from typing import List
from datetime import datetime
from .mongodb import amortizacion_collection



def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_users(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(
        username=user.username,
        email=user.email,
        nombre_completo=user.nombre_completo,
        hashed_password=hashed_password,
        is_active=user.is_active
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_creditos_for_id(db: Session, user_id: int, skip: int = 0, limit: int = 10):
    return db.query(models.Credito).filter(models.Credito.user_id == user_id).offset(skip).limit(limit).all()

def get_creditos(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Credito).offset(skip).limit(limit).all()

def create_credito(db: Session, credito: schemas.CreditoCreate, user_id: int):
    # Verificar si el usuario existe
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=400, detail=f"User with id {user_id} does not exist")

    db_credito = models.Credito(**credito.dict(), user_id=user_id)
    
    # Lógica básica de aprobación
    try:
        if credito.ingreso_mensual > credito.monto / credito.plazo:
            db_credito.aprobado = True
    except ZeroDivisionError:
        raise HTTPException(status_code=400, detail="La división por cero no está permitida")

    db.add(db_credito)
    db.commit()
    db.refresh(db_credito)
    return db_credito

def get_password_hash(password):
    return hashlib.sha256(password.encode()).hexdigest()  # Ejemplo de hash simple

# Función en CRUD para calcular el plan de amortización para varios créditos
def calcular_plan_amortizacion(creditos):
    plan_amortizaciones = []
    

    for credito in creditos:
        plan_amortizacion = []
        monto = credito.monto
        tasa_interes = credito.tasa_interes / 100 / 12  # Conversión de tasa anual a mensual
        plazo = credito.plazo

        pago_mensual = monto * (tasa_interes / (1 - (1 + tasa_interes) ** -plazo))
        saldo_restante = monto

        for mes in range(1, plazo + 1):
            intereses_pagados = saldo_restante * tasa_interes
            capital_pagado = pago_mensual - intereses_pagados
            saldo_restante -= capital_pagado

            plan_amortizacion.append({
                'mes': mes,
                'pagoMensual': round(pago_mensual, 2),
                'capitalPagado': round(capital_pagado, 2),
                'interesesPagados': round(intereses_pagados, 2),
                'saldoRestante': round(saldo_restante, 2),
                'user_id': credito.user_id
            })

        plan_amortizaciones.append({
            'id_credito': credito.id,
            'fecha_creacion': datetime.utcnow().isoformat(),
            'plan_amortizacion': plan_amortizacion,
        })
        

    print('plan_amortizaciones',plan_amortizaciones[0])
    amortizacion_collection.insert_many(plan_amortizaciones)
    print('amortizaciones completada ')

    return plan_amortizacion