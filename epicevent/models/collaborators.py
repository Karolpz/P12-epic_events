from __future__ import annotations
from typing import TYPE_CHECKING
from sqlalchemy import Integer, String, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum
from .base import Base
from argon2 import PasswordHasher

if TYPE_CHECKING:
    from .clients import Client
    from .contracts import Contract
    from .events import Event


class RoleEnum(enum.Enum):
    gestion = "gestion"
    commercial = "commercial"
    support = "support"

class Collaborator(Base):
    """Modèle représentant un collaborateur de l'entreprise."""

    __tablename__ = 'collaborators'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)

    role: Mapped[RoleEnum] = mapped_column(Enum(RoleEnum), nullable=False)

    clients: Mapped[list["Client"]] = relationship("Client", back_populates="collaborator")
    events: Mapped[list["Event"]] = relationship("Event", back_populates="collaborator")
    contracts: Mapped[list["Contract"]] = relationship("Contract", back_populates="collaborator")

    def __repr__(self):
        return f"Collaborator(id={self.id}, name={self.name}, email={self.email}, role={self.role.value})"

    def set_password(self, password):
        """Hache et enregistre le mot de passe avec Argon2."""
        ph = PasswordHasher()
        self.password = ph.hash(password)

    def verify_password(self, password):
        """Vérifie le mot de passe fourni contre le hash stocké. Retourne False en cas d'échec."""
        ph = PasswordHasher()
        try:
            return ph.verify(self.password, password)
        except Exception:
            return False