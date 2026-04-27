import socket, time
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.modules.switches.model import Switch
from app.modules.monitoring.model import AvailabilityLog

def check_switch_availability(switch: Switch):
    start_time = time.time()
    try:
        sock = socket.create_connection((switch.ip_address, switch.ssh_port), timeout=5)
        sock.close()
        latency = round((time.time() - start_time) * 1000, 2)
        if latency > 1000:
            return "warning", latency, "Respuesta lenta"
        return "online", latency, "Switch disponible"
    except socket.timeout:
        return "offline", None, "Timeout de conexión"
    except Exception as e:
        return "error", None, str(e)

def monitor_all_switches(db: Session):
    switches = db.query(Switch).all()
    for switch in switches:
        status, latency, message = check_switch_availability(switch)
        switch.status = status
        if status == "online":
            switch.last_seen_at = datetime.now(timezone.utc)
        db.add(AvailabilityLog(switch_id=switch.id, status=status, latency_ms=latency, message=message))
    db.commit()
