from sqlmodel import Field, SQLModel, create_engine, Session, select
from datetime import datetime, timezone
import pathlib

def now_utc():
    return datetime.now(timezone.utc)

class Attempt(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    challenge_id: str
    timestamp: datetime = Field(default_factory=now_utc)
    is_correct: bool
    duration: float

# Database Setup
sqlite_file_name = "leet_helix.db"
# Use a path relative to user home or current directory to avoid permission issues
DB_PATH = pathlib.Path.home() / ".leet_helix" / sqlite_file_name
DB_PATH.parent.mkdir(parents=True, exist_ok=True)
sqlite_url = f"sqlite:///{DB_PATH}"

engine = create_engine(sqlite_url)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def log_attempt(challenge_id: str, is_correct: bool, duration: float):
    with Session(engine) as session:
        attempt = Attempt(challenge_id=challenge_id, is_correct=is_correct, duration=duration)
        session.add(attempt)
        session.commit()
        session.refresh(attempt)
        return attempt

def get_attempts(challenge_id: str = None):
    with Session(engine) as session:
        statement = select(Attempt)
        if challenge_id:
            statement = statement.where(Attempt.challenge_id == challenge_id)
        results = session.exec(statement).all()
        return results

def init_db():
    create_db_and_tables()
