from app.models import Zapros
from app.schemas.zapros import ZaprosCreate
from app.repositories.base import BaseRepository

class ZaprosRepository(BaseRepository[Zapros]):
    def __init__(self, db):
        super().__init__(model=Zapros, db=db)

    def create(self, schema: ZaprosCreate) -> Zapros:
        db_obj = Zapros(**schema.model_dump())
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj