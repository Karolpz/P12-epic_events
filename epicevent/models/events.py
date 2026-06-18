from __future__ import annotations
from typing import TYPE_CHECKING
from sqlalchemy import Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from .base import Base

if TYPE_CHECKING:
    from .collaborators import Collaborator
    from .contracts import Contract

class Event(Base):
    __tablename__ = 'events'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    location: Mapped[str] = mapped_column(String(255), nullable=False)
    start_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    end_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    participants_number: Mapped[int] = mapped_column(Integer, nullable=False)
    notes: Mapped[str] = mapped_column(String(255), nullable=True)

    collaborator_id: Mapped[int] = mapped_column(Integer, ForeignKey("collaborators.id"), nullable=False)
    contract_id: Mapped[int] = mapped_column(Integer, ForeignKey("contracts.id"), nullable=True)

    collaborator: Mapped["Collaborator"] = relationship("Collaborator", back_populates="events")
    contract: Mapped["Contract"] = relationship("Contract", back_populates="event")

    def __repr__(self):
        return f"Event(id={self.id}, title={self.title}, location={self.location}, start_date={self.start_date}, end_date={self.end_date})"

    def can_edit(self, collaborator):
        return self.collaborator_id == collaborator.id

    def assign_support(self, collaborator):
        self.collaborator_id = collaborator.id