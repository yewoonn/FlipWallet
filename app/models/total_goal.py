from sqlalchemy import Column, String, DateTime, Float, Integer, ForeignKey, func
from sqlalchemy.orm import relationship

from app.models.base import Base

class TotalGoal(Base):
    __tablename__ = "total_goal"

    goal_id = Column(String(255), primary_key=True, nullable=False)
    member_id = Column(String(255), ForeignKey("member.member_id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    total_budget = Column(Float, nullable=True)
    total_expense = Column(Float, nullable=True)
    total_over = Column(Float, nullable=True, comment="여유금을 포함한 초과 금액")
    total_remaining = Column(Float, nullable=True, comment="Derived")
    member = relationship("Member", back_populates="total_goals")
