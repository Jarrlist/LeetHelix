import difflib
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax

def check_solution(user_text: str, goal_text: str) -> bool:
    """Checks if the user's solution matches the goal text."""
    return user_text.strip() == goal_text.strip()

def generate_diff(user_text: str, goal_text: str) -> str:
    """Generates a unified diff between user text and goal text."""
    diff = difflib.unified_diff(
        user_text.splitlines(),
        goal_text.splitlines(),
        fromfile="Your Solution",
        tofile="Goal Solution",
        lineterm=""
    )
    return "\n".join(diff)

def display_feedback(user_text: str, goal_text: str):
    """Displays feedback using rich."""
    console = Console()
    
    if check_solution(user_text, goal_text):
        console.print(Panel("🎉 Success! The solution is correct.", style="green bold"))
    else:
        console.print(Panel("❌ Solution incorrect. Here is the diff:", style="red bold"))
        diff_text = generate_diff(user_text, goal_text)
        syntax = Syntax(diff_text, "diff", theme="monokai", line_numbers=True)
        console.print(syntax)
