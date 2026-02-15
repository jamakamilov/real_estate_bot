from datetime import datetime, timedelta
from sqlalchemy import select
from database import async_session
from models import Listing
from config import LISTING_LIFETIME_DAYS

async def archive_old_listings():
    async with async_session() as session:
        result = await session.execute(
            select(Listing).where(
                Listing.expires_at < datetime.utcnow(),
                Listing.is_archived == False
            )
        )
        listings = result.scalars().all()

        for l in listings:
            l.is_archived = True

        await session.commit()

async def increment_views(listing_id: int):
    async with async_session() as session:
        listing = await session.get(Listing, listing_id)
        listing.views += 1
        await session.commit()

async def create_listing(user_id, title, price, city):
    async with async_session() as session:
        listing = Listing(
            owner_id=user_id,
            title=title,
            price=price,
            city=city,
            expires_at=datetime.utcnow() + timedelta(days=LISTING_LIFETIME_DAYS)
        )
        session.add(listing)
        await session.commit()
