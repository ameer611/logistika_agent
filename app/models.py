from datetime import datetime
from typing import List
from sqlalchemy import ForeignKey, String, DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from app.database import Base

class Zapros(Base):
    __tablename__ = "zaproslar"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    yuk_ortish_joyi: Mapped[str] = mapped_column(String(255), nullable=False)
    yuk_tushirish_joyi: Mapped[str] = mapped_column(String(255), nullable=False)
    yuklash_sanasi: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    
    # Avtomatik vaqtlar
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relationships
    agent_takliflari: Mapped[List["AgentTaklif"]] = relationship(back_populates="zapros")


class Malumot(Base):
    __tablename__ = "malumotlar"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    mashina_raqami: Mapped[str] = mapped_column(String(8), unique=True, nullable=False)
    joriy_lokatsiya: Mapped[str] = mapped_column(String(255), nullable=False) # Viloyat/shahar yoki GPS koordinatalar
    
    # Avtomatik vaqtlar
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relationships
    agent_takliflari: Mapped[List["AgentTaklif"]] = relationship(back_populates="mashina")


class AgentTaklif(Base):
    __tablename__ = "agent_takliflari"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    
    # Foreign Keys
    zapros_id: Mapped[int] = mapped_column(ForeignKey("zaproslar.id", ondelete="CASCADE"), nullable=False)
    mashina_id: Mapped[int] = mapped_column(ForeignKey("malumotlar.id", ondelete="CASCADE"), nullable=False)
    
    # Monitoring va vaqtlar
    zapros_yaratilgan_vaqti: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    agent_taklif_bergan_vaqti: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    # Munosabatlar (Relationships)
    zapros: Mapped["Zapros"] = relationship(back_populates="agent_takliflari")
    mashina: Mapped["Malumot"] = relationship(back_populates="agent_takliflari")