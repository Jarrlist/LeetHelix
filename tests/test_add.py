from unittest.mock import patch, MagicMock
from typer.testing import CliRunner
from leet_helix.main import app, CHALLENGES_DIR

runner = CliRunner()

def test_add_command():
    with patch("typer.prompt") as mock_prompt, \
         patch("typer.confirm") as mock_confirm, \
         patch("subprocess.run") as mock_run:
        
        # Mock user inputs
        # Title, ID, Description, Difficulty, Extension
        mock_prompt.side_effect = [
            "Test Challenge", # Title
            "test_challenge", # ID
            "Description",    # Description
            "Medium",         # Difficulty
            ".py",            # Extension
        ]
        
        # Confirm Pre-fill
        mock_confirm.return_value = True
        
        # Mock subprocess.run to simulate helix editing
        def mock_helix(args):
            # args[1] is the temp file path
            # Write something to it
            with open(args[1], "w") as f:
                f.write("edited content")
                
        mock_run.side_effect = mock_helix
        
        result = runner.invoke(app, ["add"])
        
        assert result.exit_code == 0
        assert "Challenge 'Test Challenge' created successfully" in result.stdout
        
        # Verify file creation
        challenge_path = CHALLENGES_DIR / "test_challenge.json"
        assert challenge_path.exists()
        challenge_path.unlink()
