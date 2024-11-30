from sqlalchemy import Column, String, DateTime, func, ForeignKey, Float
from app.models.base import Base

class Expense(Base):
    __tablename__ = "expense"

    expense_id = Column(String(255), primary_key=True, nullable=False)
    semi_process_id = Column(String(255), ForeignKey("semi_goal_process.semi_process_id"), nullable=False)  # 수정된 부분
    goal_id = Column(String(255), ForeignKey("total_goal.goal_id"), nullable=False)
    member_id = Column(String(255), ForeignKey("member.member_id"), nullable=False)
    price = Column(Float, nullable=True)
    item = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now(), nullable=False)