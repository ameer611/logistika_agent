from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime

class MalumotBase(BaseModel):
    mashina_raqami: str = Field(..., max_length=8, description="Mashina davlat raqami (maksimal 8 belgi, bo'shliqlarsiz)")
    joriy_lokatsiya: str

class MalumotCreate(MalumotBase):
    pass

class MalumotResponse(MalumotBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)