from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

from sqlalchemy import Column, String
from app.database import Base  # 공통 Base를 가져옵니다.