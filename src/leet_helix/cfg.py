"""This file is needed to sharing global variables across modules. 

https://docs.python.org/3/faq/programming.html#how-do-i-share-global-variables-across-modules
"""

import pathlib

import typer
from rich.console import Console

app = typer.Typer()
console = Console()

CHALLENGES_DIR = pathlib.Path(__file__).parent / "challenges_data"
REPO_URL = "https://github.com/Jarrlist/LeetHelix.git"

# Database Setup
sqlite_file_name = "leet_helix.db"

# register app's decorators
from leet_helix import app as _ 
