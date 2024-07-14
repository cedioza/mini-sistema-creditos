from sqlalchemy import Column, Integer, String, Float, Boolean
from .database import Base

class Credito(Base):
    __tablename__ = "creditos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    monto = Column(Float)
    plazo = Column(Integer)
    tasa_interes = Column(Float)
    ingreso_mensual = Column(Float)
    aprobado = Column(Boolean, default=False)
