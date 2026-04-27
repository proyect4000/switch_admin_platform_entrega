from sqlalchemy.orm import Session
from fastapi import HTTPException
from netmiko import ConnectHandler, NetmikoTimeoutException, NetmikoAuthenticationException
from app.modules.switches.model import Switch
from app.modules.ssh.command_model import CommandHistory
from app.core.encryption import decrypt_text
from app.core.config import settings

def execute_ssh_command(db: Session, user_id: int, switch_id: int, command: str):
    switch = db.query(Switch).filter(Switch.id == switch_id).first()
    if not switch:
        raise HTTPException(status_code=404, detail="Switch no encontrado")
    password = decrypt_text(switch.ssh_password_encrypted)
    device = {"device_type": "cisco_ios", "host": switch.ip_address, "username": switch.ssh_username, "password": password, "port": switch.ssh_port, "timeout": settings.SSH_TIMEOUT}
    try:
        connection = ConnectHandler(**device)
        output = connection.send_command(command)
        connection.disconnect()
        history = CommandHistory(user_id=user_id, switch_id=switch_id, command=command, output=output, success=True)
        db.add(history); db.commit()
        return {"switch_id": switch_id, "command": command, "output": output, "success": True, "error_message": None}
    except NetmikoAuthenticationException:
        error = "Error de autenticación SSH"
    except NetmikoTimeoutException:
        error = "Timeout o switch inaccesible"
    except Exception as e:
        error = str(e)
    history = CommandHistory(user_id=user_id, switch_id=switch_id, command=command, output=None, success=False, error_message=error)
    db.add(history); db.commit()
    return {"switch_id": switch_id, "command": command, "output": None, "success": False, "error_message": error}

def get_command_history(db: Session):
    return db.query(CommandHistory).order_by(CommandHistory.executed_at.desc()).limit(500).all()

def get_switch_command_history(db: Session, switch_id: int):
    return db.query(CommandHistory).filter(CommandHistory.switch_id == switch_id).order_by(CommandHistory.executed_at.desc()).limit(200).all()
