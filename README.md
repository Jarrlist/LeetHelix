# LeetHelix

Practice your Helix editor skills with code challenges.

## Installation

### For Players (Easy Install)
You can install directly from GitHub without cloning:

```bash
pip install git+https://github.com/Jarrlist/LeetHelix.git
```

### For Developers
If you want to contribute or modify the code:

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Jarrlist/LeetHelix.git
    cd leet-helix
    ```

2.  **Install in editable mode:**
    It is recommended to use a virtual environment.
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -e .
    ```

## Data Location

LeetHelix stores your progress and database in your system's standard configuration directory:

*   **Linux / macOS**: `~/.config/leet_helix/leet_helix.db` (or `$XDG_CONFIG_HOME`)
*   **Windows**: `%APPDATA%\leet_helix\leet_helix.db`

You can clear your progress by deleting this directory.

## Usage

### 1. Play

Start a challenge session. The system will intelligently select a challenge for you based on your progress.

```bash
leet play
```
Helix will open and you will get a task and hints.
When you are done just quit with :wq and your solution will be checked

```
# hello_world
# Task: Fix the print statement to output 'Hello, World!'

print('Helo, Wolrd!')


# Basic Editing:
# 1. Navigate with 'h', 'j', 'k', 'l'.
# 2. Move to typo.
# 3. Replace char: 'r' -> correct char.
# 4. Or change text: 'c' -> type -> Esc.
```

You can also play a specific challenge by its ID:

```bash
leet play <challenge_id>
```
*Example: `leet play extract_method`*


### 2. List Challenges

See all available challenges and your completion status.

```bash
leet list
```

```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━┓
┃ ID                          ┃ Difficulty ┃ Language ┃ Labels                                                              ┃ Status    ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━┩
│ edit_delete_block           │ Easy       │ python   │ select_object, edit_delete                                          │ Completed │
│ edit_replace_range          │ Easy       │ python   │ edit_change                                                         │ Completed │
│ enumerate_align             │ Medium     │ python   │ multicursor, select_regex, edit_insert, select_all                  │ Completed │
│ surround_replace_brackets   │ Easy       │ python   │ surround_replace                                                    │ Completed │
│ hello_world                 │ Easy       │ python   │ edit_insert, edit_delete, movement_basic                            │ Completed │
│ rename_variable             │ Medium     │ python   │ select_regex, edit_change                                           │ Completed │
│ surround_add_parens         │ Medium     │ python   │ surround_add, select_basic                                          │ Completed │
│ surround_delete_quotes      │ Medium     │ python   │ surround_delete, select_object, select_regex                        │ Completed │
│ snake_to_camel              │ Easy       │ python   │ edit_case, select_regex, multicursor                                │ Completed │
│ edit_join_comma             │ Medium     │ python   │ edit_join, edit_insert                                              │ Completed │
│ edit_change_object          │ Medium     │ python   │ select_object, edit_change                                          │ Completed │
│ swap_blocks                 │ Easy       │ python   │ edit_yank_paste, edit_delete, select_line                           │ Completed │
│ comment_to_list             │ Medium     │ python   │ edit_join, select_regex, multicursor, surround_add, edit_change     │ Completed │
│ search_select               │ Medium     │ python   │ search_basic, search_next, edit_change, multicursor                 │ Completed │
│ edit_case_toggle            │ Easy       │ python   │ edit_case, select_basic                                             │ Completed │
│ match_surround              │ Medium     │ python   │ surround_add, surround_replace, select_object                       │ Completed │
│ fix_indents                 │ Easy       │ python   │ edit_indent, select_line                                            │ Completed │
│ extract_function            │ Medium     │ python   │ edit_yank_paste, edit_change                                        │ Completed │
│ movement_long_jump          │ Easy       │ python   │ movement_goto, edit_change                                          │ Completed │
│ select_split_comma          │ Medium     │ python   │ select_split, edit_replace                                          │ Completed │
│ rename_variable_simple      │ Easy       │ python   │ select_regex, edit_change, search_selection, multicursor            │ Completed │
│ function_to_class           │ Hard       │ python   │ edit_change, select_regex, edit_insert, multicursor,                │ Completed │
│ surround_delete_multicursor │ Medium     │ python   │ surround_delete, multicursor                                        │ Completed │
│ edit_join_lines             │ Medium     │ python   │ edit_join, select_line                                              │ Completed │
└─────────────────────────────┴────────────┴──────────┴─────────────────────────────────────────────────────────────────────┴───────────┘
```

### 3. Stats

Check your detailed progress statistics.

```bash
leet stats
```
This menu will show you your best overall times and milestones, each level has tropyhs you get by compleating fast enough, bronze, silver, gold and author. 


```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━┓
┃ Challenge                   ┃ Status    ┃ Best Time ┃ Milestone ┃ Attempts ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━┩
│ comment_to_list             │ Completed │ 33.60s    │ 🟢 Author │ 14       │
│ edit_case_toggle            │ Completed │ 2.63s     │ 🟢 Author │ 4        │
│ edit_change_object          │ Completed │ 7.00s     │ 🟢 Author │ 4        │
│ edit_delete_block           │ Completed │ 5.67s     │ 🟢 Author │ 2        │
│ edit_join_comma             │ Completed │ 11.30s    │ 🟢 Author │ 12       │
│ edit_join_lines             │ Completed │ 2.84s     │ 🟢 Author │ 2        │
│ edit_replace_range          │ Completed │ 8.60s     │ 🟢 Author │ 4        │
│ enumerate_align             │ Completed │ 39.00s    │ 🟢 Author │ 11       │
│ extract_function            │ Completed │ 7.85s     │ 🟢 Author │ 11       │
│ fix_indents                 │ Completed │ 9.12s     │ 🟢 Author │ 4        │
│ function_to_class           │ Completed │ 41.88s    │ 🟢 Author │ 10       │
│ hello_world                 │ Completed │ 12.14s    │ 🟢 Author │ 3        │
│ match_surround              │ Completed │ 11.17s    │ 🟢 Author │ 9        │
│ movement_long_jump          │ Completed │ 6.11s     │ 🟢 Author │ 6        │
│ rename_variable             │ Completed │ 27.02s    │ 🟢 Author │ 1        │
│ rename_variable_simple      │ Completed │ 24.71s    │ 🟢 Author │ 6        │
│ search_select               │ Completed │ 10.09s    │ 🟢 Author │ 5        │
│ select_split_comma          │ Completed │ 6.78s     │ 🟢 Author │ 5        │
│ snake_to_camel              │ Completed │ 29.54s    │ 🟢 Author │ 2        │
│ surround_add_parens         │ Completed │ 7.03s     │ 🟢 Author │ 5        │
│ surround_delete_multicursor │ Completed │ 7.55s     │ 🟢 Author │ 4        │
│ surround_delete_quotes      │ Completed │ 10.29s    │ 🟢 Author │ 4        │
│ surround_replace_brackets   │ Completed │ 5.53s     │ 🟢 Author │ 4        │
│ swap_blocks                 │ Completed │ 4.33s     │ 🟢 Author │ 2        │
└─────────────────────────────┴───────────┴───────────┴───────────┴──────────┘
```

### 4. Upgrade

Keep your LeetHelix up to date to get new challenges.

```bash
leet --upgrade
```

Or manually:

```bash
pip install --upgrade git+https://github.com/Jarrlist/LeetHelix.git
```

## Development

To run the tests:

```bash
pytest
```

# Contribute
Contributions are most welcome!

## Did you find a bug? Do you think some problems or hints could be worded differently?
Create an issue or a PR with the fix.

## Do you want to add challenge, maybe a new language?
Create PR. Also, take a look at docs/ADDING_CHALLANGES.md

## Do you have some idea of a new feature, or big change?
Start a thread in the discussions or create a PR.
