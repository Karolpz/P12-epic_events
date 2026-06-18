from __future__ import annotations
from typing import TYPE_CHECKING
from sqlalchemy import Integer, Float, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from .base import Base
from epicevent.models.collaborators import RoleEnum

if TYPE_CHECKING:
    from .collaborators import Collaborator
    from .clients import Client
    from .events import Event


class Contract(Base):
    __tablename__ = 'contracts'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    amount_to_pay: Mapped[float] = mapped_column(Float, nullable=False)
    is_signed: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now)

    collaborator_id: Mapped[int] = mapped_column(Integer, ForeignKey("collaborators.id"), nullable=False)
    client_id: Mapped[int] = mapped_column(Integer, ForeignKey("clients.id"), nullable=False)

    collaborator: Mapped["Collaborator"] = relationship("Collaborator", back_populates="contracts")
    client: Mapped["Client"] = relationship("Client", back_populates="contracts")
    event: Mapped[list["Event"]] = relationship("Event", back_populates="contract")

    def __repr__(self):
        return f"Contract(id={self.id}, amount={self.amount}, amount_to_pay={self.amount_to_pay}, is_signed={self.is_signed})"

    def sign(self):
        if self.is_signed:
            raise Exception("Contrat déjà signé")
        self.is_signed = True

    def update_amount(self, amount_to_pay):
        if amount_to_pay < 0:
            raise Exception("Le montant ne peut pas être négatif")
        if amount_to_pay > self.amount:
            raise Exception("Le montant restant ne peut pas dépasser le montant total")
        self.amount_to_pay = amount_to_pay

    def can_edit(self, collaborator):
        if collaborator.role == RoleEnum.gestion:
            return True
        return self.collaborator_id == collaborator.id
