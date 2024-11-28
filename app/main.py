import os, uuid
from datetime import datetime

from sqlalchemy import create_engine, Column, String
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import sessionmaker, Session
from fastapi import FastAPI, HTTPException, Form, Depends, Request, Query
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

    if not user:
        return JSONResponse(status_code=400, content={"detail": "Invalid login ID or password"})

    # 비밀번호 해시 비교
    if not pwd_context.verify(login_request.password, user.password):
        return JSONResponse(status_code=400, content={"detail": "Invalid login ID or password"})

    # 로그인 성공 시 응답에 member_id와 name을 포함하여 반환
    return JSONResponse(
        status_code=200,
        content={
            "message": "Login successful",
            "redirect_url": "/showMyRecord",
            "member_id": user.member_id,
            "name": user.name
        }
    )


@app.post("/setSemiGoal", response_class=JSONResponse)
async def set_semi_goal(
    request: SetSemiGoalRequest,
    db: Session = Depends(get_db)
):
    try:
        # 수신된 데이터 출력
        print("수신된 데이터(JSON):", request.dict())

        # 사용자 확인
        member = db.query(Member).filter(Member.member_id == request.member_id).first()
        if not member:
            print("사용자를 찾을 수 없습니다:", request.member_id)
            raise HTTPException(status_code=404, detail="User not found")

        # 전체 목표가 이미 있는지 확인
        total_goal = db.query(TotalGoal).filter(TotalGoal.member_id == request.member_id).first()
        if not total_goal:
            # 전체 목표가 없다면 새로 생성
            total_goal = TotalGoal(
                goal_id=str(uuid.uuid4()),  # 고유한 전체 목표 ID 생성
                member_id=request.member_id,
                total_budget="0",  # 초기값 설정
                total_expense="0",
                total_over="0",
                total_remaining="0"
            )
            db.add(total_goal)
            db.commit()
            db.refresh(total_goal)

        # 카테고리 ID를 기준으로 카테고리를 찾고 세부 목표를 생성합니다.
        for category_data in request.categories:
            category = db.query(Category).filter(Category.category_id == category_data.category_id).first()
            if not category:
                print(f"카테고리를 찾을 수 없습니다: {category_data.category_id}")
                raise HTTPException(status_code=404, detail=f"Category ID '{category_data.category_id}' not found")

            # 새로운 세부 목표 추가
            new_semi_goal = SemiGoal(
                semi_id=str(uuid.uuid4()),
                semi_budget=str(category_data.budget),  # 예산 값은 문자열로 저장할 수도 있음 (데이터베이스 모델 확인 필요)
                category_id=category.category_id,
            )
            db.add(new_semi_goal)

            # 새로운 세부 목표 진행 추가
            new_semi_goal_process = SemiGoalProcess(
                semi_process_id=str(uuid.uuid4()),
                member_id=request.member_id,
                goal_id=total_goal.goal_id,
                semi_expense="0",
                semi_over="0",
                semi_remaining=str(category_data.budget),
                semi_id=new_semi_goal.semi_id
            )
            db.add(new_semi_goal_process)

        # 데이터베이스에 변경 사항 커밋
        db.commit()
        return {"message": "세부 목표와 목표 진행 데이터가 성공적으로 저장되었습니다."}

    except HTTPException as http_ex:
        print("HTTP 예외 발생:", http_ex.detail)  # HTTP 예외 메시지 로그 출력
        raise http_ex
    except Exception as e:
        print("서버에서 예외 발생:", str(e))  # 기타 예외 로그 출력
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))



@app.get("/getMyRecord")
async def get_my_record(member_id: str = Query(...), db: Session = Depends(get_db)):
    try:
        print(f"수신된 member_id: {member_id}")

        # 사용자 확인 (필요하다면 생략 가능)
        member = db.query(Member).filter(Member.member_id == member_id).first()
        if not member:
            raise HTTPException(status_code=404, detail="User not found")

        # 세부 목표 진행 상황 조회
        records = (
            db.query(SemiGoalProcess, SemiGoal, Category)
            .join(SemiGoal, SemiGoalProcess.semi_id == SemiGoal.semi_id)
            .join(Category, SemiGoal.category_id == Category.category_id)
            .filter(SemiGoalProcess.member_id == member_id)
            .all()
        )

        if not records:
            print("기록이 없습니다.")
            return {"categories": []}

        response_data = []
        for semi_process, semi_goal, category in records:
            response_data.append({
                "category_name": category.category_name,
                "color": category.category_color,
                "budget": float(semi_goal.semi_budget),
                "semi_expense": float(semi_process.semi_expense),
                "semi_remaining": float(semi_process.semi_remaining),
                "semi_over": float(semi_process.semi_over)
            })

        # 수신된 데이터를 콘솔에 출력하여 확인
        print("반환 데이터:", response_data)

        return {"categories": response_data}

    except Exception as e:
        print(f"오류 발생: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")




@app.post("/writeExpense", response_class=JSONResponse)
async def write_expense(
    request: ExpenseRequest,
    db: Session = Depends(get_db)
):
    try:
        # 수신된 데이터 확인
        print("수신된 데이터(JSON):", request.dict())

        # 사용자 확인
        member = db.query(Member).filter(Member.member_id == request.member_id).first()
        if not member:
            raise HTTPException(status_code=404, detail="User not found")

        # 세부 목표 확인
        semi_goal_process = db.query(SemiGoalProcess).filter(
            SemiGoalProcess.member_id == request.member_id,
            SemiGoalProcess.semi_id == request.semi_id
        ).first()

        if not semi_goal_process:
            raise HTTPException(status_code=404, detail=f"Semi goal not found for semi_id: {request.semi_id}")

        # Expense 데이터 생성 및 삽입
        new_expense = Expense(
            expense_id=str(uuid.uuid4()),
            semi_id=semi_goal_process.semi_id,
            goal_id=semi_goal_process.goal_id,
            member_id=request.member_id,
            price=str(request.price),
            item=request.item,
            created_at=str(datetime.datetime.now())
        )
        db.add(new_expense)

        # 잔여 예산 업데이트
        semi_goal_process.semi_expense = str(float(semi_goal_process.semi_expense) + request.price)
        semi_goal_process.semi_remaining = str(float(semi_goal_process.semi_remaining) - request.price)

        # Total-Goal 업데이트 (전체 목표 금액 차감)
        total_goal = db.query(TotalGoal).filter(TotalGoal.goal_id == semi_goal_process.goal_id).first()
        if total_goal:
            total_goal.total_expense = str(float(total_goal.total_expense) + request.price)
            total_goal.total_remaining = str(float(total_goal.total_remaining) - request.price)

        # 데이터베이스 커밋
        db.commit()

        return {"message": "지출 기록이 성공적으로 저장되었습니다."}

    except HTTPException as http_ex:
        print("HTTP 예외 발생:", http_ex.detail)
        raise http_ex
    except Exception as e:
        print("서버에서 예외 발생:", str(e))
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
