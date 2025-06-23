from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select, func
from datetime import datetime, date
import random
from models import Base, Prize, UserPrize, UserSpins
from config import config

# Создаем асинхронный движок SQLAlchemy
engine = create_async_engine(
    config.database_url or "sqlite+aiosqlite:///./prizes.db",
    echo=config.debug
)

# Создаем фабрику сессий
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

# Функция для получения сессии БД
async def get_db():
    async with async_session() as session:
        yield session

# Функция для инициализации БД
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

class Database:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def get_user_prizes(self, user_id: int) -> list[Prize]:
        """Получить все призы пользователя"""
        query = select(Prize).join(UserPrize).where(UserPrize.user_id == user_id)
        result = await self.session.execute(query)
        return result.scalars().all()
    
    async def get_spins_count(self, user_id: int, current_date: datetime) -> int:
        """Получить количество прокруток за текущий день"""
        query = select(func.count(UserSpins.id)).where(
            UserSpins.user_id == user_id,
            func.date(UserSpins.spin_date) == current_date.date()
        )
        result = await self.session.execute(query)
        return result.scalar() or 0
    
    async def get_random_prize(self) -> Prize:
        """Получить случайный приз"""
        query = select(Prize)
        result = await self.session.execute(query)
        prizes = result.scalars().all()
        return random.choice(prizes) if prizes else None
    
    async def save_user_prize(self, user_prize: UserPrize):
        """Сохранить выигранный приз"""
        self.session.add(user_prize)
        # Добавляем запись о прокрутке
        spin = UserSpins(user_id=user_prize.user_id)
        self.session.add(spin)
        await self.session.commit()
    
    async def mark_prize_withdrawn(self, user_id: int, prize_id: int):
        """Отметить приз как выведенный"""
        query = select(UserPrize).where(
            UserPrize.user_id == user_id,
            UserPrize.prize_id == prize_id,
            UserPrize.withdrawn == 0
        )
        result = await self.session.execute(query)
        prize = result.scalar_one_or_none()
        if prize:
            prize.withdrawn = 1
            await self.session.commit()
            return True
        return False 