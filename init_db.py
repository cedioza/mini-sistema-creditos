from app.database import engine
from app.models import Base, User, Credito
from faker import Faker
from sqlalchemy.orm import sessionmaker
import hashlib

def init_db():
    # Crear todas las tablas en la base de datos
    Base.metadata.create_all(bind=engine)

    # Generar datos falsos
    fake = Faker()
    Session = sessionmaker(bind=engine)
    session = Session()

    # Generar usuarios falsos
    for _ in range(10):  # Genera 10 usuarios
        username = fake.user_name()
        password = fake.password()
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        user = User(username=username, hashed_password=hashed_password)
        session.add(user)
        session.commit()  # Confirmar usuario para obtener user_id

        # Generar créditos falsos para cada usuario
        for _ in range(2):  # Genera 2 créditos por usuario
            monto = fake.random_int(min=1000, max=10000)
            plazo = fake.random_int(min=6, max=60)
            tasa_interes = fake.random_int(min=1, max=5) / 10.0
            ingreso_mensual = fake.random_int(min=500, max=5000)
            aprobado = fake.random_element(elements=[True, False])
            credito = Credito(nombre=fake.name(), monto=monto, plazo=plazo, tasa_interes=tasa_interes,
                              ingreso_mensual=ingreso_mensual, aprobado=aprobado, user_id=user.id)
            session.add(credito)

    session.commit()
    session.close()

if __name__ == "__main__":
    init_db()
