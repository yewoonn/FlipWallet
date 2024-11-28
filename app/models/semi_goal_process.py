from sqlalchemy import Column, String, ForeignKey
from app.models.base import Base

class SemiGoalProcess(Base):
    __tablename__ = "semi_goal_process"

    semi_process_id = Column(String(255), primary_key=True, nullable=False)
    member_id = Column(String(255), ForeignKey("total_goal.member_id"), primary_key=True, nullable=False)
    goal_id = Column(String(255), ForeignKey("total_goal.goal_id"), primary_key=True, nullable=False)
    semi_expense = Column(String(255), nullable=True)
    semi_over = Column(String(255), nullable=True)
    semi_remaining = Column(String(255), nullable=True)
    semi_id = Column(String(255), nullable=False)
