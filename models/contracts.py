from sqlalchemy import Integer, Float, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from .base import Base


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