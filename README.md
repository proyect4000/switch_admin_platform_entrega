# Switch Admin Platform

Sistema web institucional para registrar, monitorear y administrar switches mediante SSH.

## Accesos
- Backend: http://IP_SERVIDOR:8000
- Swagger API: http://IP_SERVIDOR:8000/docs
- Frontend: http://IP_SERVIDOR:5173
- Usuario inicial: admin@institucion.gob.pe
- Contraseña inicial: Admin123456

## Levantar rápido
```bash
cp backend/.env.example backend/.env
python3 - <<'PY'
from cryptography.fernet import Fernet
print(Fernet.generate_key().decode())
PY
# Copia la clave generada en ENCRYPTION_KEY dentro de backend/.env
docker compose up -d --build
docker compose exec backend python app/seed.py
```

## Módulos
- Login JWT
- Dashboard
- CRUD de switches
- Consola SSH WebSocket
- Mapa topológico con vis-network
- Monitoreo automático
- Historial de comandos
