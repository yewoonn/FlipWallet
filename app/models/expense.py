from sqlalchemy import Column, String, DateTime, func, ForeignKey
from app.models.base import Base

class Expense(Base):
    __tablename__ = "expense"

    expense_id = Column(String(255), primary_key=True, nullable=False)
    semi_id = Column(String(255), ForeignKey("semi_goal_process.semi_process_id"), primary_key=True, nullable=False)
    goal_id = Column(String(255), ForeignKey("semi_goal_process.goal_id"), primary_key=True, nullable=False)
    member_id = Column(String(255), ForeignKey("semi_goal_process.member_id"), primary_key=True, nullable=False)
    created_at = Column(String(255), nullable=True)
    price = Column(String(255), nullable=True)
    item = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now(), nullable=False)