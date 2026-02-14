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

CHALLENGES_DIR = pathlib.Path(__file__).parent / "challenges_data"

def get_comment_prefix(language: str) -> str:
    """Returns the comment prefix for a given language."""
    if language in ["rust", "c", "cpp", "java", "javascript", "typescript", "go"]:
        return "//"
    elif language == "sql":
        return "--"
    else: # python, ruby, shell, etc.
        return "#"

def build_file_content(challenge: dict, content: str) -> str:
    """Injects header and footer (tips) into the file content."""
    language = challenge.get("language", "python")
    comment_prefix = get_comment_prefix(language)
    
    header = f"{comment_prefix} {challenge['title']}\n"
    header += f"{comment_prefix} Task: {challenge.get('description', '')}\n\n"
    
    footer = ""
    if "tips" in challenge:
        footer += "\n\n"
        for line in challenge["tips"].splitlines():
            footer += f"{comment_prefix} {line}\n"

    return header + content + footer

def load_challenges():
    challenges = []
    # Recursively find config.json files
    for config_file in CHALLENGES_DIR.rglob("config.json"):
        try:
            with open(config_file, "r") as f:
                challenge = json.load(f)
            
            # Resolve paths relative to the config file
            challenge_dir = config_file.parent
            start_path = challenge_dir / challenge.get("start_file", "start.txt")
            goal_path = challenge_dir / challenge.get("goal_file", "goal.txt")
            
            challenge["start_path"] = start_path
            challenge["goal_path"] = goal_path
            challenge["dir_path"] = challenge_dir
            
            # For backward compatibility or convenience, we might want to read content if small
            # But the requirement is to handle potential large files, so we stick to paths mostly.
            # However, for 'list' and 'smart_select', we don't need content.
            # For 'play', we do.
            
            challenges.append(challenge)
        except Exception as e:
            console.print(f"[red]Error loading challenge from {config_file}: {e}[/red]")

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
    start_path = selected_challenge.get("start_path")
    goal_path = selected_challenge.get("goal_path")
    
    if not start_path or not start_path.exists():
        console.print(f"[red]Start file not found: {start_path}[/red]")
        return
        
    if not goal_path or not goal_path.exists():
         console.print(f"[red]Goal file not found: {goal_path}[/red]")
         return

    ext = start_path.suffix
        
    with open(start_path, "r") as f:
        start_content = f.read()

    with open(goal_path, "r") as f:
        goal_content_raw = f.read()

    # Inject header/footer to both start and goal so they are comparable
    formatted_start_content = build_file_content(selected_challenge, start_content)
    formatted_goal_content = build_file_content(selected_challenge, goal_content_raw)

    while True:
        with tempfile.NamedTemporaryFile(mode="w+", suffix=ext, delete=False) as tmp_file:
            tmp_file.write(formatted_start_content)
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

            judge_mode = selected_challenge.get("judge_mode", "exact")
            is_correct = check_solution(user_text, formatted_goal_content, judge_mode)
            duration = end_time - start_time
            
            # Log attempt to database
            log_attempt(selected_challenge["id"], is_correct, duration)

            if is_correct:
                display_feedback(user_text, formatted_goal_content, judge_mode)
                console.print(f"[bold green]🎉 Success! You completed it in {duration:.2f}s[/bold green]")
            else:
                display_feedback(user_text, formatted_goal_content, judge_mode)
                console.print(f"[bold red]❌ Failed. Duration: {duration:.2f}s[/bold red]")
            
            console.print("\n[bold]Next Challenge: j | Redo: k | Exit: esc/q[/bold]")
            
            # Wait for keypress
            while True:
                key = typer.getchar()
                if key.lower() == 'j':
                    # Find next challenge (for now just random again or handle externally)
                    # Ideally we would loop the whole play function but for now let's just break to return
                    # and maybe in future we make play() loop over challenges.
                    # As requested: "next challenge: j". 
                    # Recursively calling play() or returning to allow caller to loop?
                    # Since play takes an ID, it's a bit tricky. 
                    # Let's just exit this run and let the user run it again or pick a new one.
                    # But the user asked for "next challenge".
                    # Let's try to pick a new one.
                    
                    # We need to reload challenges and pick a new one.
                    # Simpler: just clear screen and re-run selection logic if we refactor.
                    # For now, let's just return and tell user "Loading next..."
                    
                    # Actually, better:
                    # If we wrap the challenge selection logic in a loop inside `play`, we can do it.
                    # But `play` is a command.
                    # Let's just return and implement "next" logic in a loop in main if arguments are empty.
                    # But `play` has `challenge_id` arg.
                    
                    # Let's just do a simple hack: Call `play` again without args.
                    console.print("[green]Loading next challenge...[/green]")
                    play(None) 
                    return
                    
                elif key.lower() == 'k':
                    # Redo: just break the inner loop, ensuring we re-write the temp file and open editor
                    break 
                elif key.lower() in ['q', '\x1b']: # ESC is \x1b
                    console.print("Exiting.")
                    return
                # else: ignore

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
    
    # Language prompt to organize folders
    language = typer.prompt("Language (e.g. python, rust, text)", default="python")
    
    default_ext = ".py" if language == "python" else ".txt"
    if language == "rust": default_ext = ".rs"
    
    extension = typer.prompt("File Extension", default=default_ext)
    if not extension.startswith("."):
        extension = "." + extension

    judge_mode = typer.prompt("Judge Mode (exact, ignore_whitespace, ast)", default="exact")

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

    # Create directory structure
    challenge_dir = CHALLENGES_DIR / language / challenge_id
    try:
        challenge_dir.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        console.print(f"[red]Error creating directory {challenge_dir}: {e}[/red]")
        return

    start_filename = f"start{extension}"
    goal_filename = f"goal{extension}"
    
    config_data = {
        "id": challenge_id,
        "title": title,
        "description": description,
        "difficulty": typer.prompt("Difficulty", default="Medium"),
        "language": language,
        "judge_mode": judge_mode,
        "start_file": start_filename,
        "goal_file": goal_filename
    }
    
    config_path = challenge_dir / "config.json"
    if config_path.exists():
        if not typer.confirm(f"Challenge '{challenge_id}' already exists. Overwrite?"):
            return

    with open(config_path, "w") as f:
        json.dump(config_data, f, indent=4)
        
    # Prepare content using the shared helper to ensure consistency
    # Note: build_file_content requires the challenge dict
    # We construct a temporary one or pass relevant keys
    
    # Actually, build_file_content expects a 'challenge' dict with title, description, language, tips
    # config_data has all except 'tips' (unless we added prompts for tips, which we didn't yet)
    # config_data: id, title, description, difficulty, language, judge_mode, start_file, goal_file
    
    final_start_content = build_file_content(config_data, start_text)
    final_goal_content = build_file_content(config_data, goal_text)

    # However, for 'add', we want to save the RAW content to the files (start.py, goal.py)
    # without the headers/footers, because 'play' injects them dynamically now.
    # So we should write just start_text and goal_text!
    
    with open(challenge_dir / start_filename, "w") as f:
        f.write(start_text)
        
    with open(challenge_dir / goal_filename, "w") as f:
        f.write(goal_text)
        
    console.print(f"[green]Challenge '{title}' created successfully at {challenge_dir}[/green]")

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
    challenges = load_challenges()
    table = Table("ID", "Title", "Difficulty", "Language")
    
    for c in challenges:
        table.add_row(
            c["id"], 
            c["title"], 
            c.get("difficulty", "Unknown"), 
            c.get("language", "Unknown")
        )
            
    console.print(table)

@app.command()
def init():
    """Initialize the database."""
    init_db()
    # Migration or check logic could go here, but for now we just init DB.
    console.print("[green]Database initialized.[/green]")

if __name__ == "__main__":
    app()
