"""This file encapsulates logic to working with helix editor.""" 

import subprocess

from .cfg import console

def open_editor(file_path):
    """Opens the file in Helix editor."""
    
    try:
        subprocess.run(["hx", file_path])
        return True
    except FileNotFoundError:
        console.print("[red]Error: Helix editor ('hx') not found. Please install Helix.[/red]")
        return False