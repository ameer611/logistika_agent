from pydantic import BaseModel, ConfigDict
from datetime import datetime

class ZaprosBase(BaseModel):
    yuk_ortish_joyi: str
    yuk_tushirish_joyi: str
    yuklash_sanasi: datetime

class ZaprosCreate(ZaprosBase):
    pass

class ZaprosResponse(ZaprosBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)