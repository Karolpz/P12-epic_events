from __future__ import annotations
from typing import TYPE_CHECKING
from sqlalchemy import Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from .base import Base

if TYPE_CHECKING:
    from .collaborators import Collaborator
    from .contracts import Contract


class Client(Base):
    """Modèle représentant un client de l'entreprise."""

    __tablename__ = 'clients'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    first_name: Mapped[str] = mapped_column(String(255), nullable=False)
    last_name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    company: Mapped[str] = mapped_column(String(255), nullable=False)
    phone_number: Mapped[str] = mapped_column(String(20), nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    collaborator_id: Mapped[int] = mapped_column(Integer, ForeignKey("collaborators.id"), nullable=True)

    collaborator: Mapped["Collaborator"] = relationship("Collaborator", back_populates="clients")
    contracts: Mapped[list["Contract"]] = relationship("Contract", back_populates="client")

    def __repr__(self):
        """Retourne une représentation lisible du client."""
        return f"Client(id={self.id}, first_name={self.first_name}, last_name={self.last_name}, email={self.email})"

    def can_edit(self, collaborator):
        """Retourne True si le collaborateur est le commercial responsable de ce client."""
        return self.collaborator_id == collaborator.id