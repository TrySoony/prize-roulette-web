import asyncio
from database import init_db, async_session
from models import Prize

async def init_prizes():
    async with async_session() as session:
        # Проверяем, есть ли уже призы в базе
        result = await session.execute("SELECT COUNT(*) FROM prizes")
        count = result.scalar()
        
        if count == 0:
            # Добавляем начальные призы
            prizes = [
                Prize(
                    name="Кольцо с бриллиантом",
                    image_url="/images/diamond_ring.png",
                    description="Элегантное кольцо с бриллиантом",
                    star_price=5
                ),
                Prize(
                    name="Световой меч",
                    image_url="/images/light_sword.png",
                    description="Легендарное оружие джедаев",
                    star_price=4
                ),
                Prize(
                    name="Браслет с гвоздями",
                    image_url="/images/nail_bracelet.png",
                    description="Стильный панк-аксессуар",
                    star_price=3
                ),
                Prize(
                    name="Пасхальное яйцо",
                    image_url="/images/easter_egg.png",
                    description="Волшебное яйцо с сюрпризом",
                    star_price=2
                ),
                Prize(
                    name="Шлем Неко",
                    image_url="/images/neko_helmet.png",
                    description="Защитный шлем с кошачьими ушками",
                    star_price=2
                ),
                Prize(
                    name="Любовное зелье",
                    image_url="/images/love_potion.png",
                    description="Магическое зелье любви",
                    star_price=1
                )
            ]
            
            session.add_all(prizes)
            await session.commit()
            print("Призы успешно добавлены в базу данных")
        else:
            print("Призы уже существуют в базе данных")

async def main():
    # Инициализируем структуру базы данных
    await init_db()
    # Добавляем начальные призы
    await init_prizes()

if __name__ == "__main__":
    asyncio.run(main()) 