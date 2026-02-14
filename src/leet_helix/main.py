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
import sys
import urllib.request
import re
from importlib.metadata import version, PackageNotFoundError
from datetime import datetime, timedelta, timezone
from .judge import display_feedback, check_solution
from .database import init_db, log_attempt, get_attempts

app = typer.Typer()
console = Console()

CHALLENGES_DIR = pathlib.Path(__file__).parent / "challenges_data"
REPO_URL = "https://github.com/Jarrlist/LeetHelix.git"

def get_current_version():
    try:
        return version("leet-helix")
    except PackageNotFoundError:
        return "0.0.0"

def get_latest_version():
    try:
        # We need the raw file content to read the version string.
        # Convert the repo URL to the raw content URL for pyproject.toml on the main branch.
        # From: https://github.com/User/Repo.git
        # To:   https://raw.githubusercontent.com/User/Repo/main/pyproject.toml
        # Note: If the repo is private, this will fail without a token.
        
        # Remove .git suffix if present
        repo_base = REPO_URL[:-4] if REPO_URL.endswith(".git") else REPO_URL
        raw_url = repo_base.replace("github.com", "raw.githubusercontent.com") + "/main/pyproject.toml"
        
        # GitHub requires a User-Agent header
        req = urllib.request.Request(raw_url, headers={'User-Agent': 'LeetHelix-CLI'})
        
        with urllib.request.urlopen(req, timeout=3) as response:
            content = response.read().decode()
            # extract version using regex
            match = re.search(r'version\s*=\s*"([^"]+)"', content)
            if match:
                return match.group(1)
            return None
    except Exception as e:
        # Silently fail or return None, but maybe useful to know why if debugging
        # console.print(f"[dim]Debug: failed to check version: {e}[/dim]")
        return None

def upgrade_package(force: bool = False):
    """Upgrade LeetHelix to the latest version."""
    console.print("[cyan]Checking for updates...[/cyan]")
    latest = get_latest_version()
    current = get_current_version()
    
    if not latest:
        console.print("[red]Could not fetch latest version info from GitHub.[/red]")
        if not force:
            console.print("[yellow]Use --force to force upgrade from GitHub anyway.[/yellow]")
            return
        console.print("[yellow]Force upgrading from GitHub...[/yellow]")
    elif latest == current:
        if not force:
            console.print(f"[green]You are already on the latest version ({current}).[/green]")
            return
        console.print(f"[yellow]Force reinstalling version {current}...[/yellow]")
    else:
        # Check if latest is actually newer than current
        # Simple string comparison might fail for complex versions, but for now it's okay?
        # Better to use packaging.version if available, but we don't have it in dependencies?
        # We can assume standard versioning.
        # If current > latest (e.g. dev version), we shouldn't downgrade.
        try:
            # simple split check
            l_parts = [int(x) for x in latest.split('.')]
            c_parts = [int(x) for x in current.split('.')]
            if l_parts < c_parts:
                 if not force:
                     console.print(f"[yellow]You have a newer version ({current}) than GitHub ({latest}). Not downgrading.[/yellow]")
                     return
                 console.print(f"[yellow]Force downgrading from {current} to {latest}...[/yellow]")
            else:
                 console.print(f"[yellow]Upgrading from {current} to {latest}...[/yellow]")
        except ValueError:
            # Fallback if version strings are weird
            console.print(f"[yellow]Upgrading from {current} to {latest}...[/yellow]")

    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", f"git+{REPO_URL}"])
        console.print(f"[bold green]Successfully upgraded![/bold green]")
    except subprocess.CalledProcessError as e:
        console.print(f"[red]Failed to upgrade: {e}[/red]")

@app.callback(invoke_without_command=True)
def main(ctx: typer.Context, 
         upgrade: bool = typer.Option(False, "--upgrade", help="Upgrade to latest version", is_eager=True),
         force: bool = typer.Option(False, "--force", help="Force upgrade (allow downgrade/reinstall)", is_eager=True)):
    if upgrade:
        upgrade_package(force)
        raise typer.Exit()

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
    
    header = f"{comment_prefix} {challenge['id']}\n"
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
            
            # Handle multiple goal files
            goal_files = challenge.get("goal_files", [])
            if not goal_files:
                # Fallback to single goal_file
                goal_file = challenge.get("goal_file", "goal.txt")
                if goal_file:
                     goal_files = [goal_file]
            
            goal_paths = [challenge_dir / gf for gf in goal_files]
            
            challenge["start_path"] = start_path
            challenge["goal_paths"] = goal_paths
            # Keep goal_path as the primary one for convenience/back-compat
            challenge["goal_path"] = goal_paths[0] if goal_paths else None
            challenge["dir_path"] = challenge_dir
            
            # For backward compatibility or convenience, we might want to read content if small
            # But the requirement is to handle potential large files, so we stick to paths mostly.
            # However, for 'list' and 'smart_select', we don't need content.
            # For 'play', we do.
            
            challenges.append(challenge)
        except Exception as e:
            console.print(f"[red]Error loading challenge from {config_file}: {e}[/red]")

    return challenges

def get_milestone(duration: float, author_time: float):
    """
    Returns (milestone_name, symbol, rank) based on duration and author_time.
    Rank: 4=Author, 3=Gold, 2=Silver, 1=Bronze, 0=None
    """
    if not author_time:
        return None, None, 0
        
    # Round duration to 2 decimal places to handle float precision and match display
    duration = round(duration, 2)
        
    if duration <= author_time:
        return "Author", "🟢", 4
    elif duration <= author_time * 1.25:
        return "Gold", "🥇", 3
    elif duration <= author_time * 1.75:
        return "Silver", "🥈", 2
    elif duration <= author_time * 3.0:
        return "Bronze", "🥉", 1
    return None, None, 0

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
    """
    Start a challenge session.
    
    If a challenge_id is provided, plays that specific challenge.
    Otherwise, intelligently selects a challenge based on your history.
    """
    init_db()
    
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

    console.print(f"[bold cyan]Starting Challenge: {selected_challenge['id']}[/bold cyan]")
    console.print(selected_challenge.get("description", "No description provided."))
    
    # Prepare temp file
    start_path = selected_challenge.get("start_path")
    goal_paths = selected_challenge.get("goal_paths")
    
    if not start_path or not start_path.exists():
        console.print(f"[red]Start file not found: {start_path}[/red]")
        return
    
    if not goal_paths:
         console.print(f"[red]No goal files found for challenge {selected_challenge['id']}[/red]")
         return

    ext = start_path.suffix
        
    with open(start_path, "r") as f:
        start_content = f.read()

    # Read and format ALL goals
    formatted_goals = []
    for gp in goal_paths:
        if gp.exists():
            with open(gp, "r") as f:
                content = f.read()
            formatted_goals.append(build_file_content(selected_challenge, content))
    
    if not formatted_goals:
        console.print(f"[red]Goal files exist but could not be read![/red]")
        return

    # Inject header/footer to start
    formatted_start_content = build_file_content(selected_challenge, start_content)
    # formatted_goal_content is no longer single, we have a list

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
            
            # Check against ALL goals
            is_correct = False
            matching_goal_content = None
            
            for g_content in formatted_goals:
                if check_solution(user_text, g_content, judge_mode):
                    is_correct = True
                    matching_goal_content = g_content
                    break

            duration = end_time - start_time
            
            # Check for personal best BEFORE logging the new attempt
            prev_attempts = get_attempts(selected_challenge["id"])
            prev_successes = [a for a in prev_attempts if a.is_correct]
            is_new_record = False
            prev_best_time = float('inf')
            
            if prev_successes:
                prev_best_time = min(a.duration for a in prev_successes)
                if duration < prev_best_time:
                    is_new_record = True

            # Calculate Milestones
            author_time = selected_challenge.get("author_time")
            current_ms_name, current_ms_sym, current_ms_rank = get_milestone(duration, author_time)
            
            prev_ms_rank = 0
            if prev_successes and author_time:
                 _, _, prev_ms_rank = get_milestone(prev_best_time, author_time)
            
            is_new_milestone = current_ms_rank > prev_ms_rank

            # Log attempt to database
            log_attempt(selected_challenge["id"], is_correct, duration)

            if is_correct:
                display_feedback(user_text, matching_goal_content, judge_mode)
                msg = f"[bold green]You completed it in {duration:.2f}s[/bold green]"
                if is_new_record:
                    msg += " [bold yellow]🏆 New Record Time![/bold yellow]"
                
                if is_new_milestone:
                    msg += f"\n[bold magenta]🎉 New Milestone Reached: {current_ms_sym} {current_ms_name}![/bold magenta]"
                elif current_ms_name:
                    msg += f" [{current_ms_sym} {current_ms_name}]"
                    
                console.print(msg)
            else:
                # Display feedback against PRIMARY goal (first one)
                display_feedback(user_text, formatted_goals[0], judge_mode)
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
def stats():
    """Show your progress statistics."""
    init_db()
    attempts = get_attempts()
    challenges = load_challenges()
    challenge_map = {c["id"]: c for c in challenges}
    
    if not attempts:
        console.print("[yellow]No attempts recorded yet.[/yellow]")
        return

    # --- Recent Activity (Top 20) ---
    console.print(Panel("[bold]Recent Activity (Last 20)[/bold]", expand=False))
    recent_table = Table("Time", "Challenge", "Result", "Duration")
    
    sorted_attempts = sorted(attempts, key=lambda x: x.timestamp, reverse=True)
    for attempt in sorted_attempts[:20]:
        c_id = attempt.challenge_id
        status = "[green]Pass[/green]" if attempt.is_correct else "[red]Fail[/red]"
        # Format time relative to now or just simplified date
        time_str = attempt.timestamp.strftime("%Y-%m-%d %H:%M")
        
        recent_table.add_row(
            time_str,
            c_id,
            status,
            f"{attempt.duration:.2f}s"
        )
    console.print(recent_table)
    console.print()

    # --- Best Times / Progress ---
    console.print(Panel("[bold]Challenge Progress[/bold]", expand=False))
    progress_table = Table("Challenge", "Status", "Best Time", "Milestone", "Attempts")
    
    # Group attempts by challenge
    attempts_by_id = {}
    for a in attempts:
        attempts_by_id.setdefault(a.challenge_id, []).append(a)
    
    # We want to show all challenges, or at least all attempted ones?
    # User said: "shows if you have ever compleated a test"
    # It's nicer to show all available challenges so they know what's left.
    
    # Sort challenges by id for display
    sorted_challenges = sorted(challenges, key=lambda x: x["id"])
    
    for challenge in sorted_challenges:
        c_id = challenge["id"]
        c_atts = attempts_by_id.get(c_id, [])
        author_time = challenge.get("author_time")
        
        # Calculate stats
        successful_atts = [a for a in c_atts if a.is_correct]
        is_completed = len(successful_atts) > 0
        total_count = len(c_atts)
        
        ms_display = "-"

        if is_completed:
            best_time = min(a.duration for a in successful_atts)
            best_time_str = f"[green]{best_time:.2f}s[/green]"
            status = "[bold green]Completed[/bold green]"
            
            ms_name, ms_sym, _ = get_milestone(best_time, author_time)
            if ms_name:
                ms_display = f"{ms_sym} {ms_name}"
        else:
            best_time_str = "-"
            status = "[dim]Not Solved[/dim]" if total_count > 0 else "[dim]Untouched[/dim]"
            
        progress_table.add_row(
            challenge["id"],
            status,
            best_time_str,
            ms_display,
            str(total_count)
        )
        
    console.print(progress_table)

    # Check for updates
    latest = get_latest_version()
    current = get_current_version()
    if latest and latest != current:
        console.print(f"\n[bold yellow]There is a newer version of LeetHelix out ({latest}), it might have new challenges! Use 'leet --upgrade' to upgrade.[/bold yellow]")

@app.command()
def list():
    """List all available challenges."""
    init_db()
    challenges = load_challenges()
    attempts = get_attempts()
    
    # Create a set of completed challenge IDs
    completed_ids = set()
    for a in attempts:
        if a.is_correct:
            completed_ids.add(a.challenge_id)

    table = Table("ID", "Difficulty", "Language", "Labels", "Status")
    
    for c in challenges:
        c_id = c["id"]
        # Use ID instead of title for display if needed, but we already have ID column.
        # So we just highlight ID if completed.
        display_id = c_id
        if c_id in completed_ids:
            display_id = f"[green]{c_id}[/green]"
            status = "[green]Completed[/green]"
        else:
            status = "[dim]Not Solved[/dim]"

        labels = ", ".join(c.get("tags", []))

        table.add_row(
            display_id, 
            c.get("difficulty", "Unknown"), 
            c.get("language", "Unknown"),
            labels,
            status
        )
            
    console.print(table)



if __name__ == "__main__":
    app()
