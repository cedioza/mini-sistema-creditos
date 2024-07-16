from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    nombre_completo = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True) 

    creditos = relationship("Credito", back_populates="owner")

class Credito(Base):
    __tablename__ = "creditos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)  # Nuevo campo
    monto = Column(Float, index=True)
    plazo = Column(Integer, index=True)
    tasa_interes = Column(Float, index=True)
    ingreso_mensual = Column(Float, index=True)
    aprobado = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey('users.id'))

    owner = relationship("User", back_populates="creditos")