from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from database import get_db, Database
from models import Prize, UserPrize

router = APIRouter(prefix="/api", tags=["api"])

class SpinResult(BaseModel):
    name: str
    img: str
    starPrice: int
    description: Optional[str] = None

@router.get("/prizes/{user_id}", response_model=List[SpinResult])
async def get_user_prizes(user_id: int, db: Database = Depends(get_db)):
    """Получение списка призов пользователя"""
    try:
        prizes = await db.get_user_prizes(user_id)
        return [
            SpinResult(
                name=prize.name,
                img=prize.image_url,
                starPrice=prize.star_price,
                description=prize.description
            )
            for prize in prizes
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/spin/{user_id}", response_model=SpinResult)
async def spin_roulette(user_id: int, db: Database = Depends(get_db)):
    """Крутить рулетку и получить приз"""
    try:
        # Проверка количества попыток за день
        spins_today = await db.get_spins_count(user_id, datetime.now())
        if spins_today >= 2:
            raise HTTPException(
                status_code=400,
                detail="Превышен лимит попыток на сегодня"
            )
        
        # Получение случайного приза
        prize = await db.get_random_prize()
        if not prize:
            raise HTTPException(
                status_code=404,
                detail="Призы закончились"
            )
        
        # Сохранение результата
        await db.save_user_prize(
            UserPrize(
                user_id=user_id,
                prize_id=prize.id,
                received_at=datetime.now()
            )
        )
        
        return SpinResult(
            name=prize.name,
            img=prize.image_url,
            starPrice=prize.star_price,
            description=prize.description
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 