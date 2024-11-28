from sqlalchemy import Column, String, ForeignKey
from app.models.base import Base

class Surplus(Base):
    __tablename__ = "surplus"

    surplus_id = Column(String(255), primary_key=True, nullable=False)
    goal_id = Column(String(255), ForeignKey("total_goal.goal_id"), primary_key=True, nullable=False)
    member_id = Column(String(255), ForeignKey("total_goal.member_id"), primary_key=True, nullable=False)
    surplus_budget = Column(String(255), nullable=True)
    surplus_expense = Column(String(255), nullable=True)
    surplus_remaining = Column(String(255), nullable=True)
