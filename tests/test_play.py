import json
from unittest.mock import patch, MagicMock
from typer.testing import CliRunner
from leet_helix.main import app, CHALLENGES_DIR
from sqlmodel import create_engine, SQLModel
import pytest

runner = CliRunner()

@pytest.fixture(autouse=True)
def mock_db():
    # Create an in-memory SQLite database for testing
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)
    
    # Patch the engine in the database module
    with patch("leet_helix.database.engine", engine):
        yield

def test_play_success(mock_db):
    # Create a dummy challenge for testing
    challenge_data = {
        "id": "test_challenge",
        "title": "Test Challenge",
        "description": "Test Description",
        "difficulty": "Easy",
        "start_text": "start",
        "goal_text": "goal"
    }
    
    challenge_path = CHALLENGES_DIR / "test_challenge.json"
    with open(challenge_path, "w") as f:
        json.dump(challenge_data, f)
        
    try:
        # Mock subprocess.run to simulate helix editing
        # We also need to mock reading the file back since helix won't actually edit it
        with patch("subprocess.run") as mock_run:
            def mock_helix(args):
                # args[1] is the temp file path
                with open(args[1], "w") as f:
                    f.write("goal")
            
            mock_run.side_effect = mock_helix
            
            result = runner.invoke(app, ["play", "test_challenge"])
            
            assert result.exit_code == 0, result.output
            assert "Success! The solution is correct." in result.stdout
            
    finally:
        challenge_path.unlink(missing_ok=True)

def test_play_failure(mock_db):
    # Create a dummy challenge for testing
    challenge_data = {
        "id": "test_challenge_fail",
        "title": "Test Challenge Fail",
        "description": "Test Description",
        "difficulty": "Easy",
        "start_text": "start",
        "goal_text": "goal"
    }
    
    challenge_path = CHALLENGES_DIR / "test_challenge_fail.json"
    with open(challenge_path, "w") as f:
        json.dump(challenge_data, f)
        
    try:
        with patch("subprocess.run") as mock_run:
            def mock_helix(args):
                # User leaves it as "start" (or modifies incorrectly)
                with open(args[1], "w") as f:
                    f.write("wrong")
            
            mock_run.side_effect = mock_helix
            
            result = runner.invoke(app, ["play", "test_challenge_fail"])
            
            assert result.exit_code == 0
            assert "Solution incorrect" in result.stdout
            
    finally:
        challenge_path.unlink(missing_ok=True)
