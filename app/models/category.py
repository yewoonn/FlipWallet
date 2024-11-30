from sqlalchemy import Column, String, Integer
from app.models.base import Base
from sqlalchemy.orm import relationship

class Category(Base):
    __tablename__ = "category"

    category_id = Column(Integer, primary_key=True, index=True)  # 정수형 기본 키
    category_name = Column(String)
    category_color = Column(String)

    semi_goals = relationship("SemiGoal", back_populates="category")