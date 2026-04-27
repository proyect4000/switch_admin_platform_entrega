from app.database.session import SessionLocal, engine
from app.database.base import Base
from app.modules.users.model import User
from app.modules.users.role_model import Role
from app.modules.switches.model import Switch
from app.modules.ssh.command_model import CommandHistory
from app.modules.monitoring.model import AvailabilityLog
from app.modules.topology.model import SwitchLink
from app.core.security import hash_password

Base.metadata.create_all(bind=engine)

db = SessionLocal()
roles = [
    ("Administrador", "Acceso total al sistema"),
    ("Operador", "Gestión operativa de switches"),
    ("Visor", "Solo lectura")
]
for name, description in roles:
    if not db.query(Role).filter(Role.name == name).first():
        db.add(Role(name=name, description=description))
db.commit()
admin_role = db.query(Role).filter(Role.name == "Administrador").first()
admin = db.query(User).filter(User.email == "admin@institucion.gob.pe").first()
if not admin:
    db.add(User(name="Administrador del Sistema", email="admin@institucion.gob.pe", password_hash=hash_password("Admin123456"), role_id=admin_role.id, is_active=True))
    db.commit()
db.close()
print("Base de datos inicializada. Usuario: admin@institucion.gob.pe / Admin123456")
