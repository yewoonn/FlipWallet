from sqlalchemy import Column, String, ForeignKey, Float
from app.models.base import Base

class Surplus(Base):
    __tablename__ = "surplus"

    surplus_id = Column(String(255), primary_key=True, nullable=False)
    goal_id = Column(String(255), ForeignKey("total_goal.goal_id"), nullable=False)
    member_id = Column(String(255), ForeignKey("total_goal.member_id"), nullable=False)
    surplus_budget = Column(Float, nullable=True)
    surplus_expense = Column(Float, nullable=True)
    surplus_remaining = Column(Float, nullable=True)