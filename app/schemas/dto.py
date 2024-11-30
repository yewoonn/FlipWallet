# app/schemas/dto.py
from typing import List

from pydantic import BaseModel

# 회원가입 DTO
class MemberCreate(BaseModel):
    name: str
    email: str
    login_id: str
    password: str
    confirm_password: str

# 로그인 요청 DTO
class LoginRequest(BaseModel):
    login_id: str
    password: str

# 카테고리 정보 DTO
class CategoryData(BaseModel):
    category_id: int
    budget: float

# 세부 목표 설정 요청 DTO
class SetSemiGoalRequest(BaseModel):
    member_id: str
    categories: List[CategoryData]
    surplus_budget: float

# 지출 기록 요청 DTO
class ExpenseRequest(BaseModel):
    member_id: str
    category_id: int
    item: str
    price: float