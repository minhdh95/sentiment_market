from sqlalchemy import create_engine, Column, Integer, Float, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database connection URL
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@localhost:5432/sentiment_market')

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class MarketScore(Base):
    __tablename__ = "market_scores"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, unique=True, index=True)
    score = Column(Float)
    vnindex_score = Column(Float)
    sentiment_score = Column(Float)

# Create all tables
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def save_score(score: float, vnindex_score: float, sentiment_score: float):
    db = SessionLocal()
    try:
        today = datetime.today().date()
        market_score = MarketScore(
            date=today,
            score=score,
            vnindex_score=vnindex_score,
            sentiment_score=sentiment_score
        )
        db.merge(market_score)  # Use merge to handle both insert and update
        db.commit()
    finally:
        db.close()

def get_last_score():
    db = SessionLocal()
    try:
        last_score = db.query(MarketScore).order_by(MarketScore.date.desc()).first()
        return last_score.score if last_score else None
    finally:
        db.close() 