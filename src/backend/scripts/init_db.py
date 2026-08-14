from app.db.database import engine, Base
from app.models import Tenant, User  # importe les modèles

def init_db():
    Base.metadata.create_all(bind=engine)
    print("Tables created.")

if __name__ == "__main__":
    init_db()