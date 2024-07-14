from app.database import engine
from app.models import Base

def init_db():
    # Crear todas las tablas en la base de datos
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()
