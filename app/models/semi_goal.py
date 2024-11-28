from sqlalchemy import Column, String, ForeignKey
from app.models.base import Base

class SemiGoal(Base):
    __tablename__ = "semi_goal"

    semi_id = Column(String(255), primary_key=True, nullable=False)
    semi_budget = Column(String(255), nullable=True)
    category_id = Column(String(255), ForeignKey("category.category_id"), nullable=False)
