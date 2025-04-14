from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

router = APIRouter()

# Connect to MySQL
DATABASE_URL = "mysql+mysqlconnector://root:Mano%402001@localhost:3306/gfai_db"


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# DB model


class Couple(Base):
    __tablename__ = "couples"
    id = Column(Integer, primary_key=True, index=True)
    partner1 = Column(String(100), nullable=False)
    partner2 = Column(String(100), nullable=True)
    password = Column(String(100), nullable=False)


Base.metadata.create_all(bind=engine)

# Request schemas


class SignupRequest(BaseModel):
    partner1: str
    partner2: str
    password: str


class LoginRequest(BaseModel):
    partner1: str
    password: str

# Sign Up Route


@router.post("/signup")
def signup_user(req: SignupRequest):
    db = SessionLocal()
    user = db.query(Couple).filter_by(partner1=req.partner1).first()
    if user:
        raise HTTPException(status_code=400, detail="User already exists")
    new_couple = Couple(partner1=req.partner1,
                        partner2=req.partner2, password=req.password)
    db.add(new_couple)
    db.commit()
    return {"message": "Signup successful"}

# Login Route


@router.post("/login")
def login_user(req: LoginRequest):
    db = SessionLocal()
    user = db.query(Couple).filter_by(
        partner1=req.partner1, password=req.password).first()
    if not user:
        raise HTTPException(
            status_code=401, detail="Fix the login, then I’ll fix you 😢💘")
    return {"message": "Login successful", "partner2": user.partner2}
