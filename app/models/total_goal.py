from sqlalchemy import Column, String, ForeignKey
from app.models.base import Base

class TotalGoal(Base):
    __tablename__ = "total_goal"

    goal_id = Column(String(255), primary_key=True, nullable=False)
    member_id = Column(String(255), ForeignKey("member.member_id"), primary_key=True, nullable=False)
    created_at = Column(String(255), nullable=True)
    total_budget = Column(String(255), nullable=True)
    total_expense = Column(String(255), nullable=True)
    total_over = Column(String(255), nullable=True, comment="여유금을 포함한 초과 금액")
    total_remaining = Column(String(255), nullable=True, comment="Derived")
