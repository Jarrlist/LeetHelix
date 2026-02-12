import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
import pathlib
import json
import subprocess
import tempfile
import time
import random
from datetime import datetime, timedelta, timezone
from .judge import display_feedback, check_solution
from .database import init_db, log_attempt, get_attempts

app = typer.Typer()
console = Console()

CHALLENGES_DIR = pathlib.Path(__file__).parent / "challenges"

def load_challenges():
    challenges = []
    for file in CHALLENGES_DIR.glob("*.json"):
        with open(file, "r") as f:
            challenges.append(json.load(f))
    return challenges

def select_smart_challenge(challenges):
    """Selects the next challenge based on history."""
    # Get all attempts
    # We can fetch all attempts at once or query per challenge.
    # Fetching all is better if the DB is small, which it is for now.
    all_attempts = get_attempts()
    
    # Map challenge_id -> list of attempts
    attempts_map = {c["id"]: [] for c in challenges}
    for attempt in all_attempts:
        if attempt.challenge_id in attempts_map:
            attempts_map[attempt.challenge_id].append(attempt)
            
    never_attempted = []
    failed_last = []
    solved = []
    
    for challenge in challenges:
        c_attempts = attempts_map[challenge["id"]]
        if not c_attempts:
            never_attempted.append(challenge)
            continue
            
        # Sort attempts by timestamp descending
        c_attempts.sort(key=lambda x: x.timestamp, reverse=True)
        last_attempt = c_attempts[0]
        
        if not last_attempt.is_correct:
            failed_last.append(challenge)
        else:
            solved.append((challenge, last_attempt.timestamp))
    
    if never_attempted:
        return random.choice(never_attempted)
    
    if failed_last:
        return random.choice(failed_last)
        
    if solved:
        # Return the one solved longest ago
        solved.sort(key=lambda x: x[1])
        return solved[0][0]
        
    return random.choice(challenges)

def open_editor(file_path):
    """Opens the file in Helix editor."""
    try:
        subprocess.run(["hx", file_path])
        return True
    except FileNotFoundError:
        console.print("[red]Error: Helix editor ('hx') not found. Please install Helix.[/red]")
        return False

@app.command()
def play(challenge_id: str = typer.Argument(None, help="The ID of the challenge to play")):
    """Start a challenge session."""
    
    # Load all challenges
    challenges = load_challenges()
    
    if not challenges:
        console.print("[red]No challenges found![/red]")
        return

    # Select challenge
    if challenge_id:
        # Assuming filename (without .json) is challenge_id
        selected_challenge = next((c for c in challenges if c["id"] == challenge_id), None)
        if not selected_challenge:
             console.print(f"[red]Challenge with ID {challenge_id} not found![/red]")
             return
    else:
        selected_challenge = select_smart_challenge(challenges)

    console.print(f"[bold cyan]Starting Challenge: {selected_challenge['title']}[/bold cyan]")
    console.print(selected_challenge.get("description", "No description provided."))

    # Prepare temp file
    # Determine extension based on challenge or default to .py
    # Ideally challenge json should have language/extension info
    ext = selected_challenge.get("extension", ".py")
    if not ext.startswith("."):
        ext = "." + ext
        
    with tempfile.NamedTemporaryFile(mode="w+", suffix=ext, delete=False) as tmp_file:
        tmp_file.write(selected_challenge["start_text"])
        tmp_file_path = tmp_file.name

    try:
        start_time = time.time()
        # Open in helix
        if not open_editor(tmp_file_path):
            return
        end_time = time.time()
        
        # Read edited content
        with open(tmp_file_path, "r") as f:
            user_text = f.read()

        goal_text = selected_challenge["goal_text"]
        
        display_feedback(user_text, goal_text)
        
        is_correct = check_solution(user_text, goal_text)
        duration = end_time - start_time
        
        # Log attempt to database
        log_attempt(selected_challenge["id"], is_correct, duration)

    finally:
        pathlib.Path(tmp_file_path).unlink(missing_ok=True)

@app.command()
def add():
    """Create a new challenge."""
    console.print("[bold cyan]Create a New Challenge[/bold cyan]")
    
    title = typer.prompt("Title")
    default_id = title.lower().replace(" ", "_")
    challenge_id = typer.prompt("ID", default=default_id)
    description = typer.prompt("Description")
    difficulty = typer.prompt("Difficulty", default="Medium")
    extension = typer.prompt("File Extension", default=".py")
    if not extension.startswith("."):
        extension = "." + extension

    # 1. Goal Text (The correct solution)
    console.print("[yellow]Step 1: Enter the GOAL text (the correct solution). Opening editor...[/yellow]")
    time.sleep(1.5)
    with tempfile.NamedTemporaryFile(suffix=extension, mode="w+", delete=False) as tf:
         tf_path_goal = tf.name
    
    if not open_editor(tf_path_goal):
        pathlib.Path(tf_path_goal).unlink(missing_ok=True)
        return
    
    with open(tf_path_goal, "r") as f:
         goal_text = f.read()
    pathlib.Path(tf_path_goal).unlink(missing_ok=True)
    
    if not goal_text.strip():
        console.print("[red]Goal text empty! Aborting.[/red]")
        return

    # 2. Start Text (The broken/initial state)
    console.print("[yellow]Step 2: Enter the START text (the broken code). Opening editor...[/yellow]")
    if typer.confirm("Pre-fill with goal text?", default=True):
        initial_content = goal_text
    else:
        initial_content = ""

    with tempfile.NamedTemporaryFile(suffix=extension, mode="w+", delete=False) as tf:
         tf.write(initial_content)
         tf_path_start = tf.name
    
    if not open_editor(tf_path_start):
        pathlib.Path(tf_path_start).unlink(missing_ok=True)
        return
    
    with open(tf_path_start, "r") as f:
         start_text = f.read()
    pathlib.Path(tf_path_start).unlink(missing_ok=True)

    challenge_data = {
        "id": challenge_id,
        "title": title,
        "description": description,
        "difficulty": difficulty,
        "extension": extension,
        "start_text": start_text,
        "goal_text": goal_text
    }
    
    file_path = CHALLENGES_DIR / f"{challenge_id}.json"
    if file_path.exists():
        if not typer.confirm("Challenge already exists. Overwrite?"):
            return

    with open(file_path, "w") as f:
        json.dump(challenge_data, f, indent=4)
        
    console.print(f"[green]Challenge '{title}' created successfully at {file_path}[/green]")

@app.command()
def stats():
    """Show your progress statistics."""
    attempts = get_attempts()
    if not attempts:
        console.print("[yellow]No attempts recorded yet.[/yellow]")
        return
        
    total_attempts = len(attempts)
    successful_attempts = [a for a in attempts if a.is_correct]
    failed_attempts = [a for a in attempts if not a.is_correct]
    
    success_rate = (len(successful_attempts) / total_attempts) * 100 if total_attempts > 0 else 0
    
    # Calculate unique challenges solved
    solved_challenges = set(a.challenge_id for a in successful_attempts)
    
    console.print(Panel(f"""[bold green]Statistics[/bold green]
    
Total Attempts: {total_attempts}
Success Rate: {success_rate:.1f}%
Unique Challenges Solved: {len(solved_challenges)}
""", title="Your Progress"))

    # Show recent history
    table = Table("Time", "Challenge", "Result", "Duration")
    for attempt in sorted(attempts, key=lambda x: x.timestamp, reverse=True)[:10]:
        status = "[green]Pass[/green]" if attempt.is_correct else "[red]Fail[/red]"
        table.add_row(
            attempt.timestamp.strftime("%Y-%m-%d %H:%M"),
            attempt.challenge_id,
            status,
            f"{attempt.duration:.2f}s"
        )
        
    console.print(table)

@app.command()
def list():
    """List all available challenges."""
    table = Table("ID", "Title", "Difficulty")
    
    for file in CHALLENGES_DIR.glob("*.json"):
         with open(file, "r") as f:
            data = json.load(f)
            table.add_row(data["id"], data["title"], data.get("difficulty", "Unknown"))
            
    console.print(table)

@app.command()
def init():
    """Initialize the database and challenges directory."""
    init_db()
    
    # Create example challenge if directory is empty
    if not any(CHALLENGES_DIR.iterdir()):
        example_challenge = {
            "id": "hello_world",
            "title": "Hello World Fix",
            "description": "Fix the print statement to correctly output 'Hello, World!'",
            "difficulty": "Easy",
            "start_text": "print('Helo, Wolrd!')",
            "goal_text": "print('Hello, World!')",
            "extension": ".py"
        }
        with open(CHALLENGES_DIR / "hello_world.json", "w") as f:
            json.dump(example_challenge, f, indent=4)
        console.print("[green]Created example challenge: hello_world.json[/green]")
    else:
        console.print("[yellow]Challenges directory not empty. Skipping example creation.[/yellow]")

if __name__ == "__main__":
    app()
