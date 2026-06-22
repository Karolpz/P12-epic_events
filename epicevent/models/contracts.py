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
    """Modèle représentant un contrat entre un client et l'entreprise."""

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
        """Retourne une représentation lisible du contrat."""
        return f"Contract(id={self.id}, amount={self.amount}, amount_to_pay={self.amount_to_pay}, is_signed={self.is_signed})"

    def sign(self):
        """Marque le contrat comme signé. Lève une exception si déjà signé."""
        if self.is_signed:
            raise Exception("Contrat déjà signé")
        self.is_signed = True

    def _validate_amount(self, amount):
        """Valide que le montant est positif. Lève une exception si le montant est négatif."""
        if amount < 0:
            raise Exception("Le montant ne peut pas être négatif")

    def set_amount(self, amount):
        """Définit le montant total du contrat. Lève une exception si le montant est négatif."""
        self._validate_amount(amount)
        self.amount = amount
        self.amount_to_pay = amount

    def total_amount(self, amount):
        """Met à jour le montant total du contrat et recalcule le montant restant à payer."""
        self._validate_amount(amount)
        difference = amount - self.amount
        new_amount_to_pay = self.amount_to_pay + difference
        if new_amount_to_pay < 0:
            raise Exception("Le nouveau montant total est inférieur à ce qui a déjà été payé")
        self.amount = amount
        self.amount_to_pay = new_amount_to_pay

    def update_amount(self, amount_to_pay):
        """Met à jour le montant restant à payer. Lève une exception si la valeur est invalide."""
        self._validate_amount(amount_to_pay)
        if amount_to_pay > self.amount:
            raise Exception("Le montant restant ne peut pas dépasser le montant total")
        self.amount_to_pay = amount_to_pay

    def can_edit(self, collaborator):
        """Retourne True si le collaborateur est gestionnaire ou le commercial du contrat."""
        if collaborator.role == RoleEnum.gestion:
            return True
        return self.collaborator_id == collaborator.id
