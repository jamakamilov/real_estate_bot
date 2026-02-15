from apscheduler.schedulers.asyncio import AsyncIOScheduler
from services import archive_old_listings

def start_scheduler():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(archive_old_listings, "interval", hours=12)
    scheduler.start()
