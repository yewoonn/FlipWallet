from sqlalchemy import Column, String, DateTime, func
from app.database import Base

class Member(Base):
    __tablename__ = "member"

    member_id = Column(String(255), primary_key=True, nullable=False)
    name = Column(String(255), nullable=True)
    login_id = Column(String(255), nullable=True)
    password = Column(String(255), nullable=True)
    email = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now(), nullable=False)
