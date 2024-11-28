# app/database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

# 환경 변수에서 데이터베이스 URL 로드
DATABASE_URL = "sqlite:///./test.db"

# SQLAlchemy 엔진 생성
engine = create_engine(DATABASE_URL, echo=True)

# 세션 생성
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 베이스 클래스 정의 (모든 모델이 이 Base를 상속받아야 함)
Base = declarative_base()
