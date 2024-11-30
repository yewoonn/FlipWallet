from sqlalchemy import Column, String, ForeignKey, Float, Integer
from sqlalchemy.orm import relationship

from app.models.base import Base

class SemiGoal(Base):
    __tablename__ = "semi_goal"

    semi_id = Column(String(255), primary_key=True, nullable=False)
    semi_budget = Column(Float, nullable=True)
    category_id = Column(Integer, ForeignKey("category.category_id"), nullable=False)  # 일치된 데이터 타입

    category = relationship("Category", back_populates="semi_goals")
