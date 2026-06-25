from sqlalchemy.orm import Session
from app.repositories.zapros_repo import ZaprosRepository
from app.repositories.malumot_repo import MalumotRepository
from app.repositories.taklif_repo import TaklifRepository
from app.services.ai_agent import AIAgent
from app.schemas.zapros import ZaprosCreate
from app.models import Zapros

class MatchingService:
    def __init__(self, db: Session):
        self.zapros_repo = ZaprosRepository(db)
        self.malumot_repo = MalumotRepository(db)
        self.taklif_repo = TaklifRepository(db)
        self.ai_agent = AIAgent()

    def create_new_request(self, schema: ZaprosCreate) -> Zapros:
        return self.zapros_repo.create(schema)

    def process_ai_matching(self, zapros_id: int):
        zapros = self.zapros_repo.get_by_id(zapros_id)
        if not zapros:
            return
        
        viloyat_nomi = zapros.yuk_ortish_joyi.split(" (")[0].strip()

        filtered_trucks = self.malumot_repo.get_trucks_by_viloyat(viloyat_nomi)
        if not filtered_trucks:
            print(f"{viloyat_nomi} hududida bo'sh mashina topilmadi, muqobil variantlar tekshirilmoqda...")
            filtered_trucks = self.malumot_repo.get_all()

        best_truck_id = self.ai_agent.match_truck(zapros.yuk_ortish_joyi, filtered_trucks)
        
        if best_truck_id:
            self.taklif_repo.create_taklif(
                zapros_id=zapros.id,
                mashina_id=best_truck_id,
                zapros_vaqti=zapros.created_at
            )