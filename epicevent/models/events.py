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
    """Modèle représentant un événement organisé pour un client."""

    __tablename__ = 'events'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    location: Mapped[str] = mapped_column(String(255), nullable=False)
    start_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    end_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    participants_number: Mapped[int] = mapped_column(Integer, nullable=False)
    notes: Mapped[str] = mapped_column(String(255), nullable=True)

    commercial_id: Mapped[int] = mapped_column(Integer, ForeignKey("collaborators.id"), nullable=False)
    support_id: Mapped[int] = mapped_column(Integer, ForeignKey("collaborators.id"), nullable=True)
    contract_id: Mapped[int] = mapped_column(Integer, ForeignKey("contracts.id"), nullable=True)

    commercial: Mapped["Collaborator"] = relationship("Collaborator", foreign_keys=[commercial_id])
    support: Mapped["Collaborator"] = relationship("Collaborator", foreign_keys=[support_id])
    contract: Mapped["Contract"] = relationship("Contract", back_populates="event")

    def __repr__(self):
        """Retourne une représentation lisible de l'événement."""
        return f"Event(id={self.id}, title={self.title}, location={self.location}, start_date={self.start_date}, end_date={self.end_date})"

    def can_edit(self, collaborator):
        """Retourne True si le collaborateur est le support assigné à cet événement."""
        return self.support_id == collaborator.id

    def assign_support(self, collaborator):
        """Assigne un collaborateur support à l'événement."""
        self.support_id = collaborator.id

    def set_dates(self, start_date, end_date):
        """Définit les dates de début et de fin. Lève une exception si la date de fin est avant la date de début."""
        if end_date <= start_date:
            raise Exception("La date de fin doit être après la date de début")
        self.start_date = start_date
        self.end_date = end_date