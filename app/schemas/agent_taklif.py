from pydantic import BaseModel, ConfigDict
from datetime import datetime
from .malumot import MalumotResponse

class AgentTaklifResponse(BaseModel):
    id: int
    zapros_id: int
    mashina_id: int
    zapros_yaratilgan_vaqti: datetime
    agent_taklif_bergan_vaqti: datetime
    created_at: datetime
    
    # Optionally nest the truck data
    mashina: MalumotResponse

    model_config = ConfigDict(from_attributes=True)