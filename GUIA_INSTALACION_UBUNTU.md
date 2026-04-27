# Guía para levantar Switch Admin Platform en Ubuntu Server

## 1. Requisitos mínimos

- Ubuntu Server 22.04 o 24.04
- 4 GB RAM mínimo
- 2 CPU mínimo
- Acceso a la red donde están los switches
- Puerto 22 permitido hacia switches
- Puertos del sistema:
  - 5173 frontend
  - 8000 backend
  - 5432 PostgreSQL local/contenedor

## 2. Instalar Docker

```bash
sudo apt update
sudo apt install -y docker.io docker-compose-v2 unzip python3-cryptography
sudo systemctl enable docker
sudo systemctl start docker
sudo usermod -aG docker $USER
```

Cerrar sesión y volver a ingresar.

## 3. Descomprimir proyecto

```bash
unzip switch-admin-platform-entrega.zip
cd switch_admin_platform_entrega
```

## 4. Configurar variables

```bash
cp backend/.env.example backend/.env
```

Generar clave Fernet:

```bash
python3 - <<'PY'
from cryptography.fernet import Fernet
print(Fernet.generate_key().decode())
PY
```

Editar:

```bash
nano backend/.env
```

Colocar la clave generada:

```env
ENCRYPTION_KEY=CLAVE_GENERADA
```

## 5. Levantar contenedores

```bash
docker compose up -d --build
```

## 6. Crear usuario administrador

```bash
docker compose exec backend python app/seed.py
```

Usuario inicial:

```text
admin@institucion.gob.pe
Admin123456
```

## 7. Acceder

```text
Frontend: http://IP_SERVIDOR:5173
Backend:  http://IP_SERVIDOR:8000
Swagger:  http://IP_SERVIDOR:8000/docs
```

## 8. Comandos útiles

Ver estado:

```bash
docker compose ps
```

Ver logs:

```bash
docker compose logs -f backend
docker compose logs -f frontend
```

Reiniciar:

```bash
docker compose restart
```

Bajar servicios:

```bash
docker compose down
```

## 9. Recomendación producción

Para producción institucional, colocar Nginx como proxy inverso y usar HTTPS con certificado interno o público.
