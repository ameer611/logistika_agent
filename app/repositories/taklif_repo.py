from app.models import AgentTaklif
from app.repositories.base import BaseRepository
from datetime import datetime

class TaklifRepository(BaseRepository[AgentTaklif]):
    def __init__(self, db):
        super().__init__(model=AgentTaklif, db=db)

    def create_taklif(self, zapros_id: int, mashina_id: int, zapros_vaqti: datetime) -> AgentTaklif:
        taklif = AgentTaklif(
            zapros_id=zapros_id,
            mashina_id=mashina_id,
            zapros_yaratilgan_vaqti=zapros_vaqti
        )
        self.db.add(taklif)
        self.db.commit()
        self.db.refresh(taklif)
        return taklif