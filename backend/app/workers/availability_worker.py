import asyncio
from app.database.session import SessionLocal
from app.core.config import settings
from app.modules.monitoring.service import monitor_all_switches

async def availability_worker():
    while True:
        db = SessionLocal()
        try:
            monitor_all_switches(db)
        except Exception as exc:
            print(f"[availability_worker] {exc}")
        finally:
            db.close()
        await asyncio.sleep(settings.MONITOR_INTERVAL_SECONDS)
