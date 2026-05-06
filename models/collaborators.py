from sqlalchemy import Integer, String, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum
from .base import Base


class RoleEnum(enum.Enum):
    gestion = "gestion"
    commercial = "commercial"
    support = "support"

class Collaborator(Base):
    __tablename__ = 'collaborators'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)

    role: Mapped[RoleEnum] = mapped_column(Enum(RoleEnum), nullable=False)

    clients: Mapped[list["Client"]] = relationship("Client", back_populates="collaborator")
    events: Mapped[list["Event"]] = relationship("Event", back_populates="collaborator")
    contracts: Mapped[list["Contract"]] = relationship("Contract", back_populates="collaborator")

    def __repr__(self):
        return f"Collaborator(id={self.id}, name={self.name}, email={self.email}, role={self.role.value})"