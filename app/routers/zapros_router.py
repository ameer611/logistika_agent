from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.zapros import ZaprosCreate, ZaprosResponse
from app.services.matching_service import MatchingService

router = APIRouter(prefix="/api/zaproslar", tags=["Zaproslar"])

@router.post("", response_model=ZaprosResponse, status_code=status.HTTP_201_CREATED)
def create_zapros(
    payload: ZaprosCreate, 
    background_tasks: BackgroundTasks, 
    db: Session = Depends(get_db)
):
    """Yangi zapros yaratish va backgroundda AI matchingni ishga tushirish"""
    service = MatchingService(db)
    new_zapros = service.create_new_request(payload)
    background_tasks.add_task(service.process_ai_matching, new_zapros.id)
    return new_zapros

@router.get("", response_model=List[ZaprosResponse], status_code=status.HTTP_200_OK)
def get_all_zaproslar(db: Session = Depends(get_db)):
    """Barcha yaratilgan zaproslar ro'yxatini olish"""
    service = MatchingService(db)
    # BaseRepository-dan meros olingan get_all() metodidan foydalanamiz
    return service.zapros_repo.get_all()

@router.get("/{zapros_id}", response_model=ZaprosResponse, status_code=status.HTTP_200_OK)
def get_zapros_by_id(zapros_id: int, db: Session = Depends(get_db)):
    """ID bo'yicha aniq bir zaprosni barcha ma'lumotlari bilan olish"""
    service = MatchingService(db)
    zapros = service.zapros_repo.get_by_id(zapros_id)
    
    if not zapros:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"ID {zapros_id} bo'lgan zapros topilmadi."
        )
    return zapros