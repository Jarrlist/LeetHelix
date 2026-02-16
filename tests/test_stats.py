from unittest.mock import patch, MagicMock
from typer.testing import CliRunner
from leet_helix.main import app
from datetime import datetime, timezone

runner = CliRunner()

def test_stats_empty():
    with patch("leet_helix.app.get_attempts", return_value=[]):
        result = runner.invoke(app, ["stats"])
        assert result.exit_code == 0
        assert "No attempts recorded yet" in result.stdout

def test_stats_with_data():
    now = datetime.now(timezone.utc)
    attempts = [
        MagicMock(challenge_id="c1", is_correct=True, duration=5.0, timestamp=now),
        MagicMock(challenge_id="c2", is_correct=False, duration=10.0, timestamp=now),
    ]
    
    with patch("leet_helix.app.get_attempts", return_value=attempts):
        result = runner.invoke(app, ["stats"])
        assert result.exit_code == 0
        assert "Recent Activity" in result.stdout
