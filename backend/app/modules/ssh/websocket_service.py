import asyncio
import paramiko
from fastapi import WebSocket
from sqlalchemy.orm import Session
from app.modules.switches.model import Switch
from app.core.encryption import decrypt_text

async def ssh_websocket_console(websocket: WebSocket, db: Session, switch_id: int):
    await websocket.accept()
    switch = db.query(Switch).filter(Switch.id == switch_id).first()
    if not switch:
        await websocket.send_text("ERROR: Switch no encontrado")
        await websocket.close()
        return
    password = decrypt_text(switch.ssh_password_encrypted)
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh_client.connect(hostname=switch.ip_address, port=switch.ssh_port, username=switch.ssh_username, password=password, timeout=10, look_for_keys=False, allow_agent=False)
        channel = ssh_client.invoke_shell()
        channel.settimeout(0.0)
        await websocket.send_text(f"Conectado a {switch.name} ({switch.ip_address})\n")
        async def read_from_switch():
            while True:
                if channel.recv_ready():
                    data = channel.recv(4096).decode(errors="ignore")
                    await websocket.send_text(data)
                await asyncio.sleep(0.1)
        async def write_to_switch():
            while True:
                command = await websocket.receive_text()
                channel.send(command)
        await asyncio.gather(read_from_switch(), write_to_switch())
    except Exception as e:
        await websocket.send_text(f"ERROR SSH: {str(e)}")
    finally:
        try:
            ssh_client.close()
        except Exception:
            pass
        try:
            await websocket.close()
        except Exception:
            pass
