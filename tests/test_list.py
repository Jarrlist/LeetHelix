from typer.testing import CliRunner
from unittest.mock import patch
from leet_helix.cfg import app

runner = CliRunner()

def test_list_command():
    # Mock data
    challenges = [
        {
            "id": "c1",
            "title": "Challenge 1",
            "tags": ["tag1", "tag2"],
            "difficulty": "Easy",
            "language": "python"
        },
        {
            "id": "c2",
            "title": "Challenge 2",
            "tags": [], # Empty tags
            "difficulty": "Hard",
            "language": "rust"
        }
    ]
    
    with patch("leet_helix.app.load_challenges", return_value=challenges), \
        patch("leet_helix.app.get_attempts", return_value=[]), \
        patch("leet_helix.app.init_db"):
        
        result = runner.invoke(app, ["list"])
        
        assert result.exit_code == 0
        assert "tag1, tag2" in result.stdout
        # c2 has no tags, so just check it doesn't crash and shows ID
        assert "c2" in result.stdout
