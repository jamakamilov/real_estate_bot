import asyncio
from aiogram import Bot, Dispatcher, Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from sqlalchemy import select

from config import BOT_TOKEN, ADMIN_ID, BOOST_DAYS
from database import async_session
from models import Base, User, Listing, ListingStatus, UserRole
from keyboards import approve_keyboard, boost_keyboard
from services import create_listing, increment_views
from scheduler import start_scheduler
from database import engine

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
router = Router()
dp.include_router(router)


@router.message(Command("start"))
async def start(message: Message):
    async with async_session() as session:
        user = await session.get(User, message.from_user.id)
        if not user:
            role = UserRole.admin if message.from_user.id == ADMIN_ID else UserRole.user
            session.add(User(
                id=message.from_user.id,
                username=message.from_user.username,
                role=role
            ))
            await session.commit()

    await message.answer("Добро пожаловать в бот недвижимости Чирчик")


@router.message(Command("add"))
async def add_listing(message: Message):
    parts = message.text.split("|")
    if len(parts) != 4:
        await message.answer("Формат:\n/add | Заголовок | Цена | Город")
        return

    _, title, price, city = parts

    await create_listing(
        message.from_user.id,
        title.strip(),
        int(price.strip()),
        city.strip()
    )

    await message.answer("Объявление отправлено на модерацию")


@router.message(Command("moderation"))
async def moderation(message: Message):
    if message.from_user.id != ADMIN_ID:
        return

    async with async_session() as session:
        result = await session.execute(
            select(Listing).where(Listing.status == ListingStatus.pending)
        )
        listings = result.scalars().all()

    for l in listings:
        await message.answer(
            f"{l.id}\n{l.title}\n{l.price}",
            reply_markup=approve_keyboard(l.id)
        )


@router.callback_query(F.data.startswith("approve_"))
async def approve(callback: CallbackQuery):
    listing_id = int(callback.data.split("_")[1])

    async with async_session() as session:
        listing = await session.get(Listing, listing_id)
        listing.status = ListingStatus.approved
        await session.commit()

    await callback.message.edit_text("Одобрено")


@router.message(Command("list"))
async def show_listings(message: Message):

    async with async_session() as session:
        result = await session.execute(
            select(Listing).where(
                Listing.status == ListingStatus.approved,
                Listing.is_archived == False
            ).order_by(
                Listing.is_boosted.desc(),
                Listing.created_at.desc()
            )
        )
        listings = result.scalars().all()

    for l in listings:
        await increment_views(l.id)

        await message.answer(
            f"{l.title}\n{l.price}\n{l.city}\nПросмотры: {l.views}",
            reply_markup=boost_keyboard(l.id)
        )


@router.callback_query(F.data.startswith("boost_"))
async def boost(callback: CallbackQuery):
    listing_id = int(callback.data.split("_")[1])

    async with async_session() as session:
        listing = await session.get(Listing, listing_id)
        listing.is_boosted = True
        await session.commit()

    await callback.answer("Запрос на поднятие отправлен администратору")


async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    start_scheduler()


async def main():
    await on_startup()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
