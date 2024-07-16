from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    username: str
    email: EmailStr
    nombre_completo: str
    is_active: bool = True

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int

    class Config:
        orm_mode = True

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
    user_id: int

    class Config:
        orm_mode = True

class PlanAmortizacion(BaseModel):
    mes: int
    pagoMensual: float
    capitalPagado: float
    interesesPagados: float
    saldoRestante: float
    user_id: int

    class Config:
        orm_mode = True
