from unittest.mock import patch, MagicMock
from typer.testing import CliRunner
from leet_helix.main import app, CHALLENGES_DIR

runner = CliRunner()

def test_add_command():
    with patch("typer.prompt") as mock_prompt, \
         patch("typer.confirm") as mock_confirm, \
         patch("subprocess.run") as mock_run:
        
        # Mock user inputs
        # Title, ID, Description, Language, Extension, Judge Mode
        mock_prompt.side_effect = [
            "Test Challenge", # Title
            "test_challenge", # ID
            "Description",    # Description
            "python",         # Language
            ".py",            # Extension
            "exact",          # Judge Mode
             "Medium",        # Difficulty (actually prompt order: Title, ID, Desc, Language, Ext, Judge, Difficulty? No, check main.py)
        ]
        # Checking main.py order:
        # Title, ID, Description, Language, Extension, Judge Mode, Difficulty (inside dict creation)
        
        mock_prompt.side_effect = [
            "Test Challenge", # Title
            "test_challenge", # ID
            "Description",    # Description
            "python",         # Language
            ".py",            # Extension
            "exact",          # Judge Mode
            "Medium",         # Difficulty
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
        challenge_dir = CHALLENGES_DIR / "python" / "test_challenge"
        assert challenge_dir.exists()
        assert (challenge_dir / "config.json").exists()
        assert (challenge_dir / "start.py").exists()
        assert (challenge_dir / "goal.py").exists()
        
        import shutil
        shutil.rmtree(challenge_dir)
