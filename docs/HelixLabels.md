# Helix Test Labels

This file lists the standardized labels used in challenge configurations to identify which Helix features are being tested.

## Movement
*   `movement_basic`: Basic cursor movement (h, j, k, l).
*   `movement_word`: Word-wise movement (w, b, e, W, B, E).
*   `movement_find`: Character finding (f, t, F, T).
*   `movement_goto`: Goto commands (gg, ge, gh, gl, etc.).
*   `movement_match`: Matching bracket jumps (mm).

## Editing
*   `edit_insert`: Entering insert mode (i, a, I, A, o, O).
*   `edit_delete`: Deleting text (d).
*   `edit_change`: Changing text (c).
*   `edit_replace`: Replacing characters (r, R).
*   `edit_case`: Switching case (~, `).
*   `edit_yank_paste`: Copying and pasting (y, p, P).
*   `edit_join`: Joining lines (J).
*   `edit_indent`: Indentation (<, >).

## Selection
*   `select_basic`: Basic selection mode (v).
*   `select_line`: Line selection (x).
*   `select_regex`: Regex selection within current selection (s).
*   `select_split`: Splitting selection (S).
*   `select_cursor`: Adding cursors (C).
*   `select_object`: Selecting text objects (ma, mi).
*   `select_all`: Select whole file (%).

## Search
*   `search_basic`: Basic search (/, ?).
*   `search_selection`: Search using current selection (*).
*   `search_next`: Navigating matches (n, N).

## Surround
*   `surround_add`: Adding surround (ms).
*   `surround_replace`: Replacing surround (mr).
*   `surround_delete`: Deleting surround (md).

## Advanced
*   `multicursor`: Using multiple cursors effectively.
*   `macro`: Recording and replaying macros (q, Q).
