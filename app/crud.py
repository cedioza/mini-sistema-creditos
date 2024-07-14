from sqlalchemy.orm import Session
from . import models, schemas

def create_credito(db: Session, credito: schemas.CreditoCreate):
    db_credito = models.Credito(
        nombre=credito.nombre,
        monto=credito.monto,
        plazo=credito.plazo,
        tasa_interes=credito.tasa_interes,
        ingreso_mensual=credito.ingreso_mensual,
        aprobado=credito.ingreso_mensual >= credito.monto / credito.plazo * 3
    )
    db.add(db_credito)
    db.commit()
    db.refresh(db_credito)
    return db_credito

def get_creditos(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Credito).offset(skip).limit(limit).all()
