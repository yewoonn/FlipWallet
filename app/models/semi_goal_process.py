from sqlalchemy import Column, String, ForeignKey, Float, Integer
from sqlalchemy.orm import relationship
from app.models.base import Base

class SemiGoalProcess(Base):
    __tablename__ = "semi_goal_process"

    semi_process_id = Column(String(255), primary_key=True, nullable=False)
    member_id = Column(String(255), ForeignKey("total_goal.member_id"), nullable=False)
    goal_id = Column(String(255), ForeignKey("total_goal.goal_id"), nullable=False)
    semi_expense = Column(Float, nullable=True)
    semi_over = Column(Float, nullable=True)
    semi_remaining = Column(Float, nullable=True)
    semi_id = Column(String(255), ForeignKey("semi_goal.semi_id"), nullable=False)
    semi_goal = relationship("SemiGoal")
