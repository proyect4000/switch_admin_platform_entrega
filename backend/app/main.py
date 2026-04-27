import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.database.session import engine
from app.database.base import Base
from app.modules.users.model import User
from app.modules.users.role_model import Role
from app.modules.switches.model import Switch
from app.modules.ssh.command_model import CommandHistory
from app.modules.monitoring.model import AvailabilityLog
from app.modules.topology.model import SwitchLink
from app.modules.auth.router import router as auth_router
from app.modules.switches.router import router as switches_router
from app.modules.ssh.router import router as ssh_router
from app.modules.ssh.websocket_router import router as ssh_ws_router
from app.modules.topology.router import router as topology_router
from app.modules.monitoring.router import router as monitoring_router
from app.modules.dashboard.router import router as dashboard_router
from app.workers.availability_worker import availability_worker

app = FastAPI(title=settings.APP_NAME, description="Sistema web para administración y monitoreo de switches vía SSH", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(switches_router)
app.include_router(ssh_router)
app.include_router(ssh_ws_router)
app.include_router(topology_router)
app.include_router(monitoring_router)
app.include_router(dashboard_router)

@app.on_event("startup")
async def startup_event():
    Base.metadata.create_all(bind=engine)
    asyncio.create_task(availability_worker())

@app.get("/")
def health_check():
    return {"status": "ok", "message": "Switch Admin Platform API funcionando correctamente"}
