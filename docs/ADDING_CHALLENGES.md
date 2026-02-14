# Adding New Challenges to LeetHelix

This guide details the process of creating new challenges for LeetHelix. It is designed for developers and AI agents to ensure consistency and quality across the challenge suite.

**IMPORTANT FOR AI AGENTS:**
If you discover new patterns, best practices, or constraints (e.g., "avoid % selection"), you **MUST** update this file to reflect what you have learned. Keep this document living and accurate.

## 📂 Directory Structure

Challenges are organized by programming language within the `src/leet_helix/challenges_data` directory.

```
src/leet_helix/challenges_data/
├── python/
│   ├── challenge_id_1/
│   │   ├── config.json
│   │   ├── start.py
│   │   └── goal.py
│   └── challenge_id_2/
│       └── ...
├── rust/
│   └── ...
└── ...
```

## 📝 Required Files

Each challenge folder **must** contain exactly these three files:

1.  **`config.json`**: Metadata and configuration.
2.  **`start.ext`** (e.g., `start.py`): The initial code state provided to the user.
3.  **`goal.ext`** (e.g., `goal.py`): The target code state (the correct solution).

### 1. `config.json`

This is the control file. It must be valid JSON with the following structure:

```json
{
    "id": "unique_snake_case_id",
    "title": "Human Readable Title",
    "description": "A concise (1 sentence) description of the task.",
    "difficulty": "Easy" | "Medium" | "Hard",
    "language": "python",
    "judge_mode": "ast" | "exact" | "ignore_whitespace",
    "start_file": "start.py",
    "goal_file": "goal.py",
    "tips": "Step-by-step hints using Helix commands.\nKeep lines under 80 chars.\nUse \\n for newlines.",
    "tags": [
        "tag_from_helix_labels_md",
        "another_tag"
    ]
}
```

#### Fields Detail:

*   **`id`**: Unique identifier, snake_case (e.g., `extract_method`). Matches folder name.
*   **`title`**: Displayed in the menu (e.g., "Extract Method").
*   **`description`**: Brief objective. **MUST** state *what* needs to be changed (e.g., "Change 100 to 200"). Do not rely on tips to convey the goal.
*   **`difficulty`**: Subjective difficulty level.
*   **`language`**: The programming language ID (used for folder structure and syntax highlighting).
*   **`judge_mode`**:
    *   `"ast"`: (Recommended for code) Parses code into an Abstract Syntax Tree. Ignores whitespace/comments differences. *Python only.*
    *   `"exact"`: Byte-for-byte comparison. Hardest mode.
    *   `"ignore_whitespace"`: Strips whitespace before comparing. Good for text manipulation.
*   **`tips`**: A string containing hints.
    *   **Formatting**: Use `\n` for line breaks.
    *   **Constraint**: Keep lines **< 80 characters** to prevent terminal wrapping issues.
    *   **Content**: Explicitly mention the Helix keys. Teach the most efficient/idiomatic method (e.g., use `mr` to replace brackets, not delete+insert).
*   **`tags`**: A list of feature tags. **MUST** come from `HelixLabels.md`.

### 2. `start.py` & `goal.py`

*   **Content Only**: Do **not** include the challenge description header (e.g., `# Task: ...`) or the tips footer. The game engine injects these automatically during gameplay to ensure consistent formatting.
*   **Clean Code**: Ensure the code is valid (parses correctly) so AST comparison works.
*   **Minimal Diff**: Try to keep the `start` and `goal` files similar enough that the diff is readable, but different enough to require specific Helix actions.

## ✅ Quality Guidelines

Creating high-quality challenges ensures users learn effectively. Follow these principles:

1.  **Realism**:
    *   Code should look like real code. Define variables before using them (e.g., `a = 1`, `b = 2` before `L = [a, b]`).
    *   Avoid nonsensical snippets like `foo bar baz` unless strictly necessary for a text manipulation task.
    *   Functions should have bodies, even if just `pass` or print statements.

2.  **Appropriate Context**:
    *   **Length**: For movement challenges (e.g., `movement_long_jump`), ensure the file is actually long (50+ lines) so the jump is useful.
    *   **Structure**: For object selection (e.g., `maf`), make the block large enough that selecting it manually would be tedious.

3.  **Syntactic Validity**:
    *   Ensure both `start.py` and `goal.py` are valid, parseable code.
    *   This is critical for `judge_mode: "ast"` to work correctly.

4.  **Justification**:
    *   The task should demonstrate *why* the Helix feature is useful.
    *   Example: Don't ask to delete 3 lines to teach `maf`. Ask to delete a 20-line function.

5.  **Instruction vs. Hint Separation**:
    *   **Description**: Must tell the user *what* to achieve (e.g., "Wrap the expression in parentheses").
    *   **Tips**: Must tell the user *how* to achieve it (e.g., "Use 'ms('").
    *   Do not hide the goal inside the tips.

6.  **Idiomatic Helix**:
    *   Teach the "Helix way". If a task can be done with `mr` (match replace), don't teach `d` then `i`.
    *   If a tip uses a specific feature (e.g., `s` for regex selection), ensure the corresponding tag (`select_regex`) is present in `config.json`.
    *   **Specific Commands**: If using `gw` (jump to label), be precise. It is not just "goto word".

7.  **Selection Strategy**:
    *   **Avoid `%`**: In the game environment, the file includes a description header and tips footer. Using `%` selects these artifacts, which breaks many transformation commands.
    *   **Use Specific Selectors**: Teach `vip` (select inner paragraph), `x` (select line), or `mi...` (select inside object) to target the user's code block specifically.

8.  **Robustness & Anti-Cheating**:
    *   **Vary Values**: When asking to change multiple occurrences, ensure the values differ (e.g., `timeout=30`, `timeout=6000`). This prevents simple Find/Replace (`%s`) or macro solutions from being too easy and forces structural navigation.
    *   **Mix Types**: Use combinations of lists, tuples, and dicts. This prevents "gaming" the challenge by searching for a single closing delimiter (like `)`) to find the end of a block.
    *   **Noise**: Add "noisy" content (e.g., strings containing parentheses) to break simple regex searches if the goal is structural navigation (`mm`).

## ⚠️ Common Pitfalls

*   **`exact` Judge Mode**: Avoid this unless spacing is strictly part of the challenge. It frustrates users when a trailing newline fails the solution. Use `ast` (Python) or `ignore_whitespace` (Text) instead.
*   **Vague Instructions**: "Fix the code" is bad. "Change the function name to 'process'" is good.
*   **Overwhelming Tips**: Don't dump 5 different ways to do it. Teach the *best* way.
*   **Short Files**: Helix shines in large files. One-liners don't demonstrate the power of `gw` or `mip`.
*   **Uniform Data**: "Change all `foo` to `bar`" is often better solved with `%s/foo/bar`. "Remove the 2nd argument from these 3 different function calls" forces cursor movement and specific edits.

## 🗺️ Roadmap: Missing Features

We need challenges for these Helix features:

1.  **Macros (`q`, `Q`)**: Recording and replaying complex edits.
2.  **Registers (`"`)**: Yanking to named registers (`"ay`) and pasting (`"ap`).
3.  **Selection Filtering (`K`, `Alt-K`)**: Keeping/removing cursors matching a regex.
4.  **Shell Piping (`|`)**: Sorting lines or formatting via external CLI tools.

## 🏷️ Tags & Categories

We use a standardized list of tags to categorize challenges by the Helix features they test.

*   **Source of Truth**: Refer to `docs/HelixLabels.md` in the project root.
*   **Selection**: Always verify tags against that file. Do not invent new tags without updating `docs/HelixLabels.md` first.

**Common Tags:**
*   `movement_basic`, `movement_word`, `movement_find`, `movement_goto`
*   `edit_insert`, `edit_delete`, `edit_change`, `edit_replace`, `edit_case`, `edit_join`, `edit_comment`
*   `select_line`, `select_regex`, `select_object`, `select_syntax`
*   `search_basic`, `search_selection`
*   `surround_add`, `surround_replace`
*   `multicursor`

## 📚 Resources

*   **`docs/HelixFeatures.md`**: (Project Root) A dump of Helix features and documentation. Use this to understand *what* is possible.
*   **`docs/HelixLabels.md`**: (Project Root) The official registry of tags. Use this to label your challenges.
*   **`tutor` files**: Look for `tutor` or `helixTutor.txt` in the repo for inspiration on teaching sequences.

## 🚀 Workflow for Agents

1.  **Plan**: Identify a Helix feature to teach (e.g., "Multiple Cursors").
2.  **Consult & Update Labels**: 
    *   Check `docs/HelixLabels.md` for the correct tag (e.g., `multicursor`). 
    *   **Crucial**: If the feature (e.g., "Comment" `Ctrl-c`) is missing, you **MUST** add it to `docs/HelixLabels.md` first. Do not use an incorrect tag or invent one without documentation.
3.  **Draft**: Create the `start` and `goal` code.
    *   *Tip*: For `multicursor`, ensure there are aligned patterns in `start.py` that make vertical selection or regex selection obvious.
4.  **Configure**: Create `config.json`.
    *   Set `judge_mode` appropriately (usually `ast` for Python).
    *   Write `tips` that guide the user through the specific key sequence (e.g., "1. Select lines. 2. Press 's'. ...").
5.  **Verify**:
    *   Are lines < 80 chars?
    *   Are headers removed from `start`/`goal` files?
    *   Are tags valid?
    *   Does the tip avoid selecting the whole file with `%`?
