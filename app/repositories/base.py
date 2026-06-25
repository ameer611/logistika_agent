from typing import Generic, TypeVar, Type, List, Optional
from sqlalchemy.orm import Session
from app.database import Base


ModelType = TypeVar("ModelType", bound=Base)

class BaseRepository(Generic[ModelType]):
    def __init__(self, model: Type[ModelType], db: Session):
        self.model = model
        self.db = db

    # Umumiy ID orqali topish funksiyasi
    def get_by_id(self, id: int) -> Optional[ModelType]:
        return self.db.query(self.model).filter(self.model.id == id).first()

    # Umumiy barcha ma'lumotlarni olish funksiyasi
    def get_all(self) -> List[ModelType]:
        return self.db.query(self.model).all()

    # Umumiy o'chirish funksiyasi
    def delete(self, id: int) -> bool:
        obj = self.get_by_id(id)
        if obj:
            self.db.delete(obj)
            self.db.commit()
            return True
        return False