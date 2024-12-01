import os, uuid
from datetime import datetime

from sqlalchemy import create_engine, Column, String
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import sessionmaker, Session
from fastapi import FastAPI, HTTPException, Form, Depends, Request, Query, status
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from passlib.context import CryptContext  # bcrypt를 사용하기 위한 라이브러리

# 모든 모델을 명시적으로 임포트
from app.schemas.dto import MemberCreate, CategoryData, SetSemiGoalRequest, LoginRequest, ExpenseRequest
from app.database import engine, Base, SessionLocal
from app.models.member import Member
from app.models.total_goal import TotalGoal
from app.models.semi_goal import SemiGoal
from app.models.semi_goal_process import SemiGoalProcess
from app.models.category import Category
from app.models.expense import Expense
from app.models.surplus import Surplus

# FastAPI 애플리케이션 생성
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 출처 허용 (배포 시 특정 출처로 제한 필요)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 절대 경로 설정
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 프로젝트 루트 경로
TEMPLATES_DIR = os.path.join(PROJECT_ROOT, "app", "templates")  # templates 폴더 절대 경로 지정
STATIC_DIR = os.path.join(PROJECT_ROOT, "app", "static")  # static 폴더 절대 경로 지정
# 템플릿 설정
templates = Jinja2Templates(directory=TEMPLATES_DIR)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# bcrypt 설정
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 비밀번호 해시 함수
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# 회원가입 라우터 등록

# 데이터베이스 세션 의존성 주입 함수
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 데이터베이스 파일이 없을 때만 생성
if not os.path.exists(os.path.join(PROJECT_ROOT, "..", "test.db")):
    Base.metadata.create_all(bind=engine)
#####################################################################
#####################################################################
#####################################################################
"""
#1. GET으로 페이지 불러오기 
"""
# 0. 메인 화면
@app.get("/", response_class=HTMLResponse)
async def main_page(request: Request):
    return templates.TemplateResponse("main.html", {"request": request})

# 1. 회원가입 페이지
@app.get("/signup", response_class=HTMLResponse)
async def get_signup_page(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

# 2. 로그인 페이지
@app.get("/login", response_class=HTMLResponse)
async def get_login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

# 3. 영수증 업로드 페이지
@app.get("/receiptRecord", response_class=HTMLResponse)
async def get_receipt_record_page(request: Request):
    return templates.TemplateResponse("receiptRecord.html", {"request": request})

# 4. 세부 목표 설정 페이지
@app.get("/setSemiGoal", response_class=HTMLResponse)
async def get_set_semi_goal_page(request: Request):
    return templates.TemplateResponse("setSemiGoal.html", {"request": request})

# 5. 나의 지출 기록 페이지
@app.get("/showMyRecord", response_class=HTMLResponse)
async def get_show_my_record_page(request: Request):
    return templates.TemplateResponse("showMyRecord.html", {"request": request})

# 6. 지출 기록 페이지
@app.get("/writeExpense", response_class=HTMLResponse)
async def get_write_expense_page(request: Request):
    return templates.TemplateResponse("writeExpense.html", {"request": request})
#####################################################################
#####################################################################
#####################################################################
"""
#2. POST 요청 보내기
"""
@app.post("/signup", response_class=HTMLResponse)
async def signup(
    request: Request,
    signup_data: MemberCreate,
    db: Session = Depends(get_db)
):
    # 비밀번호 확인 (백엔드 검증)
    if signup_data.password != signup_data.confirm_password:
        return templates.TemplateResponse("signup.html", {"request": request, "error": "Passwords do not match"})

    # 이메일 또는 아이디 중복 확인
    existing_user = db.query(Member).filter((Member.email == signup_data.email) | (Member.login_id == signup_data.login_id)).first()
    if existing_user:
        return templates.TemplateResponse("signup.html", {"request": request, "error": "Email or Login ID already registered"})

    # 비밀번호 해시화 (암호화)
    hashed_password = hash_password(signup_data.password)

    # 회원 생성
    new_member = Member(
        member_id=str(uuid.uuid4()),  # UUID를 사용하여 고유한 회원 ID 생성
        name=signup_data.name,
        email=signup_data.email,
        login_id=signup_data.login_id,
        password=hashed_password,  # 해시된 비밀번호 저장
    )

    # 데이터베이스에 사용자 추가
    db.add(new_member)
    db.commit()
    db.refresh(new_member)

    # 회원가입 완료 후 setSemiGoal 페이지로 리다이렉트
    return RedirectResponse(url="/setSemiGoal", status_code=303)


@app.post("/login")
async def login(login_request: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(Member).filter(Member.login_id == login_request.login_id).first()

    # 해시 비교까지 한번에 진행
    if not user or not pwd_context.verify(login_request.password, user.password):
        return JSONResponse(status_code=400, content={"detail": "Invalid login ID or password"})

    return JSONResponse(
        status_code=200,
        content={
            "message": "Login successful",
            "redirect_url": "/",
            "member_id": user.member_id,
            "name": user.name
        }
    )




@app.post("/setSemiGoal", response_class=JSONResponse)
async def set_semi_goal(request: SetSemiGoalRequest, db: Session = Depends(get_db)):
    try:
        print("수신된 데이터(JSON):", request.dict())

        # Member 확인
        member = db.query(Member).filter(Member.member_id == request.member_id).first()
        if not member:
            raise HTTPException(status_code=404, detail="User not found")

        # Total Goal 확인 또는 생성
        total_goal = db.query(TotalGoal).filter(TotalGoal.member_id == request.member_id).first()
        if not total_goal:
            total_goal = TotalGoal(
                goal_id=str(uuid.uuid4()),
                member_id=request.member_id,
                created_at=datetime.now(),
                total_budget=0.0,  # 전체 예산 초기값
                total_expense=0.0,
                total_over=0.0,
                total_remaining=0.0
            )
            db.add(total_goal)
            db.commit()
            db.refresh(total_goal)

        # 세부 목표 설정
        total_budget = 0.0  # 전체 예산을 계산하기 위한 변수
        for category_data in request.categories:
            # 기존에 SemiGoal이 있는지 확인
            semi_goal = db.query(SemiGoal).filter(SemiGoal.category_id == category_data.category_id).first()

            if not semi_goal:
                # SemiGoal을 새로 생성
                semi_goal = SemiGoal(
                    semi_id=str(uuid.uuid4()),
                    semi_budget=category_data.budget,
                    category_id=category_data.category_id
                )
                db.add(semi_goal)
                db.commit()
                db.refresh(semi_goal)

            # 기존에 SemiGoalProcess가 있는지 확인
            semi_goal_process = db.query(SemiGoalProcess).filter(
                SemiGoalProcess.member_id == request.member_id,
                SemiGoalProcess.goal_id == total_goal.goal_id,
                SemiGoalProcess.semi_id == semi_goal.semi_id
            ).first()

            if semi_goal_process:
                # 이미 존재하는 경우 업데이트
                semi_goal_process.semi_remaining = category_data.budget
                semi_goal_process.semi_expense = 0.0
            else:
                # 새로운 SemiGoalProcess 생성
                new_semi_goal_process = SemiGoalProcess(
                    semi_process_id=str(uuid.uuid4()),
                    member_id=request.member_id,
                    goal_id=total_goal.goal_id,
                    semi_expense=0.0,
                    semi_remaining=category_data.budget,
                    semi_id=semi_goal.semi_id
                )
                db.add(new_semi_goal_process)

            # 총 예산에 각 카테고리 예산 추가
            total_budget += category_data.budget

        # 비상금을 전체 예산에 추가
        total_budget += request.surplus_budget

        # TotalGoal 업데이트
        total_goal.total_budget = total_budget
        total_goal.total_remaining = total_budget  # 초기에는 남은 금액이 전체 예산과 동일
        db.commit()

        return {"message": "세부 목표와 목표 진행 데이터가 성공적으로 저장되었습니다."}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"서버 오류 발생: {str(e)}")




@app.get("/getMyRecord")
async def get_my_record(member_id: str = Query(...), db: Session = Depends(get_db)):
    try:
        print(f"수신된 member_id: {member_id}")

        # 사용자 확인
        member = db.query(Member).filter(Member.member_id == member_id).first()
        if not member:
            raise HTTPException(status_code=404, detail="User not found")

        # TotalGoal 데이터 가져오기
        total_goal = db.query(TotalGoal).filter(TotalGoal.member_id == member_id).first()
        if not total_goal:
            return {"categories": [], "total_budget": 0}

        # 세부 목표 진행 상황 조회
        records = (
            db.query(SemiGoalProcess, SemiGoal, Category)
            .join(SemiGoal, SemiGoalProcess.semi_id == SemiGoal.semi_id, isouter=True)
            .join(Category, SemiGoal.category_id == Category.category_id, isouter=True)
            .filter(SemiGoalProcess.member_id == member_id)
            .all()
        )

        response_data = []
        for semi_process, semi_goal, category in records:
            response_data.append({
                "category_name": category.category_name if category else "Unknown Category",
                "color": category.category_color if category else "#000000",
                "budget": float(semi_goal.semi_budget) if semi_goal and semi_goal.semi_budget else 0.0,
                "semi_expense": float(semi_process.semi_expense) if semi_process and semi_process.semi_expense else 0.0,
                "semi_remaining": float(
                    semi_process.semi_remaining) if semi_process and semi_process.semi_remaining else 0.0,
                "semi_over": float(semi_process.semi_over) if semi_process and semi_process.semi_over else 0.0
            })

        # 반환 값에 total_budget 추가
        return {
            "categories": response_data,
            "total_budget": total_goal.total_budget  # 전체 예산을 추가로 반환
        }

    except Exception as e:
        print(f"오류 발생: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")






@app.post("/writeExpense", response_class=JSONResponse)
async def write_expense(expense_request: ExpenseRequest, db: Session = Depends(get_db)):
    try:
        # Member 확인
        member = db.query(Member).filter(Member.member_id == expense_request.member_id).first()
        if not member:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Member not found")

        # SemiGoal과 Category를 기반으로 SemiGoalProcess 찾기
        semi_goal = db.query(SemiGoal).filter(SemiGoal.category_id == expense_request.category_id).first()
        if not semi_goal:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Semi goal not found for category_id")

        # 해당 member_id와 연결된 SemiGoalProcess 찾기
        semi_goal_process = db.query(SemiGoalProcess).filter(
            SemiGoalProcess.semi_id == semi_goal.semi_id,
            SemiGoalProcess.member_id == expense_request.member_id
        ).first()

        if not semi_goal_process:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Semi goal process not found for category_id: {expense_request.category_id} and member_id: {expense_request.member_id}"
            )

        # Expense 데이터 생성 및 삽입
        new_expense = Expense(
            expense_id=str(uuid.uuid4()),
            semi_process_id=semi_goal_process.semi_process_id,
            goal_id=semi_goal_process.goal_id,
            member_id=expense_request.member_id,
            price=expense_request.price,
            item=expense_request.item,
            created_at=datetime.now()
        )
        db.add(new_expense)

        # 잔여 금액 및 초과 금액 계산
        semi_remaining = semi_goal_process.semi_remaining or 0  # None이면 0으로 처리
        semi_over = semi_goal_process.semi_over or 0  # None이면 0으로 처리

        remaining = semi_remaining - expense_request.price
        if remaining < 0:
            semi_goal_process.semi_remaining = 0
            semi_goal_process.semi_over = semi_over + abs(remaining)  # 초과 금액 추가
        else:
            semi_goal_process.semi_remaining = remaining

        semi_goal_process.semi_expense += expense_request.price

        # Total-Goal 업데이트
        total_goal = db.query(TotalGoal).filter(TotalGoal.goal_id == semi_goal_process.goal_id).first()
        if total_goal:
            total_expense = total_goal.total_expense or 0  # None이면 0으로 처리
            total_remaining = total_goal.total_remaining or 0  # None이면 0으로 처리
            total_over = total_goal.total_over or 0  # None이면 0으로 처리

            total_goal.total_expense = total_expense + expense_request.price
            remaining_total = total_remaining - expense_request.price
            if remaining_total < 0:
                total_goal.total_remaining = 0
                total_goal.total_over = total_over + abs(remaining_total)
            else:
                total_goal.total_remaining = remaining_total

        db.commit()
        return {"message": "지출 기록이 성공적으로 저장되었습니다."}

    except HTTPException as http_ex:
        print("HTTP 예외 발생:", http_ex.detail)
        raise http_ex
    except Exception as e:
        print("서버에서 예외 발생:", str(e))
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
