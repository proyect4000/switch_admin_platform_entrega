# Instalación en Ubuntu Server

```bash
sudo apt update
sudo apt install -y docker.io docker-compose-v2 git python3-cryptography
sudo systemctl enable docker
sudo systemctl start docker
```

```bash
unzip switch-admin-platform-entrega.zip
cd switch_admin_platform_entrega
cp backend/.env.example backend/.env
python3 - <<'PY'
from cryptography.fernet import Fernet
print(Fernet.generate_key().decode())
PY
```

Copie la clave generada en `ENCRYPTION_KEY`.

```bash
docker compose up -d --build
docker compose exec backend python app/seed.py
```

Acceso:

- Frontend: `http://IP_SERVIDOR:5173`
- Backend: `http://IP_SERVIDOR:8000`
- Swagger: `http://IP_SERVIDOR:8000/docs`
