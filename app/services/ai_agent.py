from typing import List, Optional

from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

from app.config import settings
from app.models import Malumot


class TruckSelection(BaseModel):
    selected_truck_id: int = Field(
        description="The exact ID of the selected truck from the available trucks list."
    )


class AIAgent:
    def __init__(self):
        self.llm = ChatOllama(
            model=settings.OLLAMA_MODEL,
            temperature=0,
            base_url=settings.OLLAMA_API_URL
        )

        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """
                    You are a professional logistics dispatch system. 
                    Your ONLY job is to select one truck ID from the provided list that is mathematically closest to the shipment origin.
                    
                    Rules:
                    1. Parse the latitude and longitude inside the parentheses for both the origin and the trucks.
                    2. Calculate the closest proximity based on these coordinates.
                    3. You MUST pick an ID that exists in the provided trucks list. Do not invent any IDs.
                    4. Output must strictly follow the required tool schema.
                    """,
                ),
                (
                    "human",
                    """
                    Shipment origin point:
                    {origin}

                    List of available trucks in this region:
                    {trucks}

                    Select the single best truck ID.
                    """,
                ),
            ]
        )

        # with_structured_output funktsiyani chaqirishni kafolatlaydi
        self.chain = (
            self.prompt
            | self.llm.with_structured_output(TruckSelection)
        )

    def match_truck(
        self,
        origin: str,
        trucks: List[Malumot]
    ) -> Optional[int]:

        if not trucks:
            return None

        # Haqiqatda mavjud ID'lar to'plami (Validation uchun)
        valid_truck_ids = {truck.id for truck in trucks}

        # Modelga ketadigan ma'lumotni soddalashtiramiz
        trucks_data = [
            {
                "id": truck.id,
                "location": truck.joriy_lokatsiya,
            }
            for truck in trucks
        ]

        try:
            # AI modelni chaqirish
            result: TruckSelection = self.chain.invoke(
                {
                    "origin": origin,
                    "trucks": trucks_data,
                }
            )

            # AI qaytargan ID haqiqatda ro'yxatda borligini tekshiramiz
            if result and result.selected_truck_id in valid_truck_ids:
                return result.selected_truck_id
            
            print(f"AI returned invalid truck ID: {result.selected_truck_id if result else 'None'}. Fallback applied.")
            return trucks[0].id

        except Exception as exc:
            print(f"AI matching error: {exc}. Using fallback first truck.")
            # Har qanday holatda ham tizim to'xtab qolmasligi uchun birinchi truck ID sini qaytaramiz
            return trucks[0].id