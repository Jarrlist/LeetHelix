from sqlmodel import Field, SQLModel, create_engine, Session, select
from datetime import datetime, timezone
import pathlib
import os
import sys

def now_utc():
    return datetime.now(timezone.utc)

class Attempt(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    challenge_id: str
    timestamp: datetime = Field(default_factory=now_utc)
    is_correct: bool
    duration: float

# Database Setup
def get_config_dir() -> pathlib.Path:
    """Returns the platform-specific configuration directory."""
    app_name = "leet_helix"
    if sys.platform == "win32":
        # Windows: Use %APPDATA%/leet_helix
        app_data = os.getenv("APPDATA")
        if app_data:
            return pathlib.Path(app_data) / app_name
        return pathlib.Path.home() / ("." + app_name)
    else:
        # macOS / Linux: Use ~/.config/leet_helix (or XDG_CONFIG_HOME)
        xdg_config = os.getenv("XDG_CONFIG_HOME")
        if xdg_config:
            return pathlib.Path(xdg_config) / app_name
        return pathlib.Path.home() / ".config" / app_name

sqlite_file_name = "leet_helix.db"
config_dir = get_config_dir()
DB_PATH = config_dir / sqlite_file_name

# Ensure the directory exists
try:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
except Exception as e:
    # Fallback to home directory if permission denied or other error
    print(f"Warning: Could not create config dir at {DB_PATH.parent}. Using ~/.leet_helix instead.")
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
