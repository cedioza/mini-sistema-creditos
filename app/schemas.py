from pydantic import BaseModel

class CreditoBase(BaseModel):
    nombre: str
    monto: float
    plazo: int
    tasa_interes: float
    ingreso_mensual: float

class CreditoCreate(CreditoBase):
    pass

class Credito(CreditoBase):
    id: int
    aprobado: bool

    class Config:
        orm_mode = True
