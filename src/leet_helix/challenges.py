import json
import random

from .cfg import console, CHALLENGES_DIR
from .database import get_attempts

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
            
            # Handle extra files (for multi-file challenges)
            extra_files = challenge.get("extra_files", [])
            extra_file_paths = [challenge_dir / ef for ef in extra_files]

            # Handle multi-file validation
            validation = challenge.get("validation", {})
            validation_map = {}
            for filename, goal_filename in validation.items():
                validation_map[filename] = challenge_dir / goal_filename

            challenge["start_path"] = start_path
            challenge["goal_paths"] = goal_paths
            # Keep goal_path as the primary one for convenience/back-compat
            challenge["goal_path"] = goal_paths[0] if goal_paths else None
            challenge["dir_path"] = challenge_dir
            challenge["extra_file_paths"] = extra_file_paths
            challenge["validation_map"] = validation_map
            
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

