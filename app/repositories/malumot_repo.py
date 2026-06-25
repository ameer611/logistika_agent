from typing import List
from app.models import Malumot
from app.repositories.base import BaseRepository

class MalumotRepository(BaseRepository[Malumot]):
    def __init__(self, db):
        super().__init__(model=Malumot, db=db)
    
    def get_trucks_by_viloyat(self, viloyat_nomi: str) -> List[Malumot]:
        """Bazadan joriy_lokatsiyasida viloyat nomi bor mashinalarni qidirib qaytaradi"""
        return self.db.query(self.model).filter(
            self.model.joriy_lokatsiya.like(f"%{viloyat_nomi}%")
        ).all()