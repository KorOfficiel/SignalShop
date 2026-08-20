from app.db.database import SessionLocal
from app.models.tenant import Tenant
from app.models.user import User
from app.core.security import get_password_hash
import uuid

def create_initial_owner():
    db = SessionLocal()
    try:
        # Récupérer ou créer le tenant par défaut
        tenant = db.query(Tenant).first()
        if not tenant:
            tenant = Tenant(id=uuid.uuid4(), name="Default Tenant", timezone="Europe/Paris")
            db.add(tenant)
            db.commit()
            db.refresh(tenant)

        # Vérifier si l'utilisateur admin existe déjà
        admin_user = db.query(User).filter(User.email == "admin@example.com").first()
        if admin_user:
            print("L'utilisateur admin existe déjà. Mise à jour du mot de passe.")
            admin_user.hashed_password = get_password_hash("admin1234")
            admin_user.role = "OWNER"
            db.commit()
        else:
            new_user = User(
                id=uuid.uuid4(),
                tenant_id=tenant.id,
                email="admin@example.com",
                hashed_password=get_password_hash("admin1234"),
                full_name="Admin",
                role="OWNER"
            )
            db.add(new_user)
            db.commit()
            print("Utilisateur OWNER créé : admin@example.com / admin1234")
    finally:
        db.close()

if __name__ == "__main__":
    create_initial_owner()