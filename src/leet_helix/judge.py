"""This file encapsulates logic to check solutions to the challenges.""" 

import difflib
import ast
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax

def normalize_code(code: str) -> str:
    """Normalizes code by stripping whitespace from lines and removing empty lines."""
    return "\n".join([line.strip() for line in code.splitlines() if line.strip()])

def check_solution_ast(user_text: str, goal_text: str) -> bool:
    """Checks if the user's solution matches the goal text using AST comparison."""
    try:
        user_ast = ast.parse(user_text)
        goal_ast = ast.parse(goal_text)
        return ast.dump(user_ast) == ast.dump(goal_ast)
    except SyntaxError:
        return False

def check_solution(user_text: str, goal_text: str, judge_mode: str = "exact") -> bool:
    """Checks if the user's solution matches the goal text."""
    if judge_mode == "ast":
        return check_solution_ast(user_text, goal_text)
    elif judge_mode == "ignore_whitespace":
        return normalize_code(user_text) == normalize_code(goal_text)
    else: # "exact"
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

def display_feedback(user_text: str, goal_text: str, judge_mode: str = "exact"):
    """Displays feedback using rich."""
    console = Console()
    
    if check_solution(user_text, goal_text, judge_mode):
        console.print(Panel("🎉 Success! The solution is correct.", style="green bold"))
    else:
        console.print(Panel("❌ Solution incorrect. Here is the diff:", style="red bold"))
        # Always show diff for now, maybe improve this for AST later
        diff_text = generate_diff(user_text, goal_text)
        syntax = Syntax(diff_text, "diff", theme="monokai", line_numbers=True)
        console.print(syntax)
        if judge_mode == "ast":
             console.print("[yellow]Note: Judge mode is AST. Structure must match exactly, but formatting (whitespace) is flexible.[/yellow]")
