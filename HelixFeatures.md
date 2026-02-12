Registers
User-defined registers
Default registers
Special registers
In Helix, registers are storage locations for text and other data, such as the result of a search. Registers can be used to cut, copy, and paste text, similar to the clipboard in other text editors. Usage is similar to Vim, with " being used to select a register.

User-defined registers
Helix allows you to create your own named registers for storing text, for example:

"ay - Yank the current selection to register a.
"op - Paste the text in register o after the selection.
If a register is selected before invoking a change or delete command, the selection will be stored in the register and the action will be carried out:

"hc - Store the selection in register h and then change it (delete and enter insert mode).
"md - Store the selection in register m and delete it.
Default registers
Commands that use registers, like yank (y), use a default register if none is specified. These registers are used as defaults:

Register character	Contains
/	Last search
:	Last executed command
"	Last yanked text
@	Last recorded macro
Special registers
Some registers have special behavior when read from and written to.

Register character	When read	When written
_	No values are returned	All values are discarded
#	Selection indices (first selection is 1, second is 2, etc.)	This register is not writable
.	Contents of the current selections	This register is not writable
%	Name of the current file	This register is not writable
+	Reads from the system clipboard	Joins and yanks to the system clipboard
*	Reads from the primary clipboard	Joins and yanks to the primary clipboard
When yanking multiple selections to the clipboard registers, the selections are joined with newlines. Pasting from these registers will paste multiple selections if the clipboard was last yanked to by the Helix session. Otherwise the clipboard contents are pasted as one selection.



Surround
Helix includes built-in functionality similar to vim-surround. The keymappings have been inspired from vim-sandwich:

Surround demo

Key Sequence	Action
ms<char> (after selecting text)	Add surround characters to selection
mr<char_to_replace><new_char>	Replace the closest surround characters
md<char_to_delete>	Delete the closest surround characters
You can use counts to act on outer pairs.

Surround can also act on multiple selections. For example, to change every occurrence of (use) to [use]:

% to select the whole file
s to split the selections on a search term
Input use and hit Enter
mr([ to replace the parentheses with square brackets
Multiple characters are currently not supported, but planned for future release.


Selecting and manipulating text with textobjects
In Helix, textobjects are a way to select, manipulate and operate on a piece of text in a structured way. They allow you to refer to blocks of text based on their structure or purpose, such as a word, sentence, paragraph, or even a function or block of code.

Textobject demo Textobject tree-sitter demo

ma - Select around the object (va in Vim, <alt-a> in Kakoune)
mi - Select inside the object (vi in Vim, <alt-i> in Kakoune)
Key after mi or ma	Textobject selected
w	Word
W	WORD
p	Paragraph
(, [, ', etc.	Specified surround pairs
m	The closest surround pair
f	Function
t	Type (or Class)
a	Argument/parameter
c	Comment
T	Test
g	Change
💡 f, t, etc. need a tree-sitter grammar active for the current document and a special tree-sitter query file to work properly. Only some grammars currently have the query file implemented. Contributions are welcome!

Navigating using tree-sitter textobjects
Navigating between functions, classes, parameters, and other elements is possible using tree-sitter and textobject queries. For example to move to the next function use ]f, to move to previous type use [t, and so on.

Tree-sitter-nav-demo

For the full reference see the unimpaired section of the key bind documentation.

💡 This feature relies on tree-sitter textobjects and requires the corresponding query file to work properly.



Moving the selection with syntax-aware motions
Alt-p, Alt-o, Alt-i, and Alt-n (or Alt and arrow keys) allow you to move the selection according to its location in the syntax tree. For example, many languages have the following syntax for function calls:

func(arg1, arg2, arg3);
A function call might be parsed by tree-sitter into a tree like the following.

(call
  function: (identifier) ; func
  arguments:
    (arguments           ; (arg1, arg2, arg3)
      (identifier)       ; arg1
      (identifier)       ; arg2
      (identifier)))     ; arg3
Use :tree-sitter-subtree to view the syntax tree of the primary selection. In a more intuitive tree format:

            ┌────┐
            │call│
      ┌─────┴────┴─────┐
      │                │
┌─────▼────┐      ┌────▼────┐
│identifier│      │arguments│
│  "func"  │ ┌────┴───┬─────┴───┐
└──────────┘ │        │         │
             │        │         │
   ┌─────────▼┐  ┌────▼─────┐  ┌▼─────────┐
   │identifier│  │identifier│  │identifier│
   │  "arg1"  │  │  "arg2"  │  │  "arg3"  │
   └──────────┘  └──────────┘  └──────────┘
If you have a selection that wraps arg1 (see the tree above), and you use Alt-n, it will select the next sibling in the syntax tree: arg2.

// before
func([arg1], arg2, arg3)
// after
func(arg1, [arg2], arg3);
Similarly, Alt-o will expand the selection to the parent node, in this case, the arguments node.

func[(arg1, arg2, arg3)];
There is also some nuanced behavior that prevents you from getting stuck on a node with no sibling. When using Alt-p with a selection on arg1, the previous child node will be selected. In the event that arg1 does not have a previous sibling, the selection will move up the syntax tree and select the previous element. As a result, using Alt-p with a selection on arg1 will move the selection to the "func" identifier.


Using pickers
Helix has a variety of pickers, which are interactive windows used to select various kinds of items. These include a file picker, global search picker, and more. Most pickers are accessed via keybindings in space mode. Pickers have their own keymap for navigation.

Filtering Picker Results
Most pickers perform fuzzy matching using fzf syntax. Two exceptions are the global search picker, which uses regex, and the workspace symbol picker, which passes search terms to the language server. Note that OR operations (|) are not currently supported.

If a picker shows multiple columns, you may apply the filter to a specific column by prefixing the column name with %. Column names can be shortened to any prefix, so %p, %pa or %pat all mean the same as %path. For example, a query of helix %p .toml !lang in the global search picker searches for the term "helix" within files with paths ending in ".toml" but not including "lang".

You can insert the contents of a register using Ctrl-r followed by a register name. For example, one could insert the currently selected text using Ctrl-r-., or the directory of the current file using Ctrl-r-% followed by Ctrl-w to remove the last path section. The global search picker will use the contents of the search register if you press Enter without typing a filter. For example, pressing *-Space-/-Enter will start a global search for the currently selected text.



Keymap
Normal mode
Movement
Changes
Shell
Selection manipulation
Search
Minor modes
View mode
Goto mode
Match mode
Window mode
Space mode
Popup
Completion Menu
Signature-help Popup
Unimpaired
Insert mode
Select / extend mode
Picker
Prompt
💡 Mappings marked (LSP) require an active language server for the file.

💡 Mappings marked (TS) require a tree-sitter grammar for the file type.

⚠️ Some terminals' default key mappings conflict with Helix's. If any of the mappings described on this page do not work as expected, check your terminal's mappings to ensure they do not conflict. See the wiki for known conflicts.

Normal mode
Normal mode is the default mode when you launch helix. You can return to it from other modes by pressing the Escape key.

Movement
NOTE: Unlike Vim, f, F, t and T are not confined to the current line.

Key	Description	Command
h, Left	Move left	move_char_left
j, Down	Move down	move_visual_line_down
k, Up	Move up	move_visual_line_up
l, Right	Move right	move_char_right
w	Move next word start	move_next_word_start
b	Move previous word start	move_prev_word_start
e	Move next word end	move_next_word_end
W	Move next WORD start	move_next_long_word_start
B	Move previous WORD start	move_prev_long_word_start
E	Move next WORD end	move_next_long_word_end
t	Find till next char	find_till_char
f	Find next char	find_next_char
T	Find till previous char	till_prev_char
F	Find previous char	find_prev_char
G	Go to line number <n>	goto_line
Alt-.	Repeat last motion (f, t, m, [ or ])	repeat_last_motion
Home	Move to the start of the line	goto_line_start
End	Move to the end of the line	goto_line_end
Ctrl-b, PageUp	Move page up	page_up
Ctrl-f, PageDown	Move page down	page_down
Ctrl-u	Move cursor and page half page up	page_cursor_half_up
Ctrl-d	Move cursor and page half page down	page_cursor_half_down
Ctrl-i	Jump forward on the jumplist	jump_forward
Ctrl-o	Jump backward on the jumplist	jump_backward
Ctrl-s	Save the current selection to the jumplist	save_selection
Changes
Key	Description	Command
r	Replace with a character	replace
R	Replace with yanked text	replace_with_yanked
~	Switch case of the selected text	switch_case
`	Set the selected text to lower case	switch_to_lowercase
Alt-`	Set the selected text to upper case	switch_to_uppercase
i	Insert before selection	insert_mode
a	Insert after selection (append)	append_mode
I	Insert at the start of the line	insert_at_line_start
A	Insert at the end of the line	insert_at_line_end
o	Open new line below selection	open_below
O	Open new line above selection	open_above
.	Repeat last insert	N/A
u	Undo change	undo
U	Redo change	redo
Alt-u	Move backward in history	earlier
Alt-U	Move forward in history	later
y	Yank selection	yank
p	Paste after selection	paste_after
P	Paste before selection	paste_before
" <reg>	Select a register to yank to or paste from	select_register
>	Indent selection	indent
<	Unindent selection	unindent
=	Format selection (LSP)	format_selections
d	Delete selection	delete_selection
Alt-d	Delete selection, without yanking	delete_selection_noyank
c	Change selection (delete and enter insert mode)	change_selection
Alt-c	Change selection (delete and enter insert mode, without yanking)	change_selection_noyank
Ctrl-a	Increment object (number) under cursor	increment
Ctrl-x	Decrement object (number) under cursor	decrement
Q	Start/stop macro recording to the selected register (experimental)	record_macro
q	Play back a recorded macro from the selected register (experimental)	replay_macro
Shell
Key	Description	Command
|	Pipe each selection through shell command, replacing with output	shell_pipe
Alt-|	Pipe each selection into shell command, ignoring output	shell_pipe_to
!	Run shell command, inserting output before each selection	shell_insert_output
Alt-!	Run shell command, appending output after each selection	shell_append_output
$	Pipe each selection into shell command, keep selections where command returned 0	shell_keep_pipe
Selection manipulation
Key	Description	Command
s	Select all regex matches inside selections	select_regex
S	Split selection into sub selections on regex matches	split_selection
Alt-s	Split selection on newlines	split_selection_on_newline
Alt-minus	Merge selections	merge_selections
Alt-_	Merge consecutive selections	merge_consecutive_selections
&	Align selection in columns	align_selections
_	Trim whitespace from the selection	trim_selections
;	Collapse selection onto a single cursor	collapse_selection
Alt-;	Flip selection cursor and anchor	flip_selections
Alt-:	Ensures the selection is in forward direction	ensure_selections_forward
,	Keep only the primary selection	keep_primary_selection
Alt-,	Remove the primary selection	remove_primary_selection
C	Copy selection onto the next line (Add cursor below)	copy_selection_on_next_line
Alt-C	Copy selection onto the previous line (Add cursor above)	copy_selection_on_prev_line
(	Rotate main selection backward	rotate_selections_backward
)	Rotate main selection forward	rotate_selections_forward
Alt-(	Rotate selection contents backward	rotate_selection_contents_backward
Alt-)	Rotate selection contents forward	rotate_selection_contents_forward
%	Select entire file	select_all
x	Select current line, if already selected, extend to next line	extend_line_below
X	Extend selection to line bounds (line-wise selection)	extend_to_line_bounds
Alt-x	Shrink selection to line bounds (line-wise selection)	shrink_to_line_bounds
J	Join lines inside selection	join_selections
Alt-J	Join lines inside selection and select the inserted space	join_selections_space
K	Keep selections matching the regex	keep_selections
Alt-K	Remove selections matching the regex	remove_selections
Ctrl-c	Comment/uncomment the selections	toggle_comments
Alt-o, Alt-up	Expand selection to parent syntax node (TS)	expand_selection
Alt-i, Alt-down	Shrink syntax tree object selection (TS)	shrink_selection
Alt-p, Alt-left	Select previous sibling node in syntax tree (TS)	select_prev_sibling
Alt-n, Alt-right	Select next sibling node in syntax tree (TS)	select_next_sibling
Alt-a	Select all sibling nodes in syntax tree (TS)	select_all_siblings
Alt-I, Alt-Shift-down	Select all children nodes in syntax tree (TS)	select_all_children
Alt-e	Move to end of parent node in syntax tree (TS)	move_parent_node_end
Alt-b	Move to start of parent node in syntax tree (TS)	move_parent_node_start
Search
Search commands all operate on the / register by default. To use a different register, use "<char>.

Key	Description	Command
/	Search for regex pattern	search
?	Search for previous pattern	rsearch
n	Select next search match	search_next
N	Select previous search match	search_prev
*	Use current selection as the search pattern, automatically wrapping with \b on word boundaries	search_selection_detect_word_boundaries
Alt-*	Use current selection as the search pattern	search_selection
Minor modes
These sub-modes are accessible from normal mode and typically switch back to normal mode after a command.

Key	Description	Command
v	Enter select (extend) mode	select_mode
g	Enter goto mode	N/A
m	Enter match mode	N/A
:	Enter command mode	command_mode
z	Enter view mode	N/A
Z	Enter sticky view mode	N/A
Ctrl-w	Enter window mode	N/A
Space	Enter space mode	N/A
These modes (except command mode) can be configured by remapping keys.

View mode
Accessed by typing z in normal mode.

View mode is intended for scrolling and manipulating the view without changing the selection. The "sticky" variant of this mode (accessed by typing Z in normal mode) is persistent and can be exited using the escape key. This is useful when you're simply looking over text and not actively editing it.

Key	Description	Command
z, c	Vertically center the line	align_view_center
t	Align the line to the top of the screen	align_view_top
b	Align the line to the bottom of the screen	align_view_bottom
m	Align the line to the middle of the screen (horizontally)	align_view_middle
j, down	Scroll the view downwards	scroll_down
k, up	Scroll the view upwards	scroll_up
Ctrl-f, PageDown	Move page down	page_down
Ctrl-b, PageUp	Move page up	page_up
Ctrl-u	Move cursor and page half page up	page_cursor_half_up
Ctrl-d	Move cursor and page half page down	page_cursor_half_down
Goto mode
Accessed by typing g in normal mode.

Jumps to various locations.

Key	Description	Command
g	Go to line number <n> else start of file	goto_file_start
|	Go to column number <n> else start of line	goto_column
e	Go to the end of the file	goto_last_line
f	Go to files in the selections	goto_file
h	Go to the start of the line	goto_line_start
l	Go to the end of the line	goto_line_end
s	Go to first non-whitespace character of the line	goto_first_nonwhitespace
t	Go to the top of the screen	goto_window_top
c	Go to the middle of the screen	goto_window_center
b	Go to the bottom of the screen	goto_window_bottom
d	Go to definition (LSP)	goto_definition
y	Go to type definition (LSP)	goto_type_definition
r	Go to references (LSP)	goto_reference
i	Go to implementation (LSP)	goto_implementation
a	Go to the last accessed/alternate file	goto_last_accessed_file
m	Go to the last modified/alternate file	goto_last_modified_file
n	Go to next buffer	goto_next_buffer
p	Go to previous buffer	goto_previous_buffer
.	Go to last modification in current file	goto_last_modification
j	Move down textual (instead of visual) line	move_line_down
k	Move up textual (instead of visual) line	move_line_up
w	Show labels at each word and select the word that belongs to the entered labels	goto_word
Match mode
Accessed by typing m in normal mode.

Please refer to the relevant sections for detailed explanations about surround and textobjects.

Key	Description	Command
m	Goto matching bracket (TS)	match_brackets
s <char>	Surround current selection with <char>	surround_add
r <from><to>	Replace surround character <from> with <to>	surround_replace
d <char>	Delete surround character <char>	surround_delete
a <object>	Select around textobject	select_textobject_around
i <object>	Select inside textobject	select_textobject_inner
TODO: Mappings for selecting syntax nodes (a superset of [).

Window mode
Accessed by typing Ctrl-w in normal mode.

This layer is similar to Vim keybindings as Kakoune does not support windows.

Key	Description	Command
w, Ctrl-w	Switch to next window	rotate_view
v, Ctrl-v	Vertical right split	vsplit
s, Ctrl-s	Horizontal bottom split	hsplit
f	Go to files in the selections in horizontal splits	goto_file
F	Go to files in the selections in vertical splits	goto_file
h, Ctrl-h, Left	Move to left split	jump_view_left
j, Ctrl-j, Down	Move to split below	jump_view_down
k, Ctrl-k, Up	Move to split above	jump_view_up
l, Ctrl-l, Right	Move to right split	jump_view_right
q, Ctrl-q	Close current window	wclose
o, Ctrl-o	Only keep the current window, closing all the others	wonly
H	Swap window to the left	swap_view_left
J	Swap window downwards	swap_view_down
K	Swap window upwards	swap_view_up
L	Swap window to the right	swap_view_right
Space mode
Accessed by typing Space in normal mode.

This layer is a kludge of mappings, mostly pickers.

Key	Description	Command
f	Open file picker at LSP workspace root	file_picker
F	Open file picker at current working directory	file_picker_in_current_directory
b	Open buffer picker	buffer_picker
j	Open jumplist picker	jumplist_picker
g	Open changed file picker	changed_file_picker
G	Debug (experimental)	N/A
k	Show documentation for item under cursor in a popup (LSP)	hover
s	Open document symbol picker (LSP)	symbol_picker
S	Open workspace symbol picker (LSP)	workspace_symbol_picker
d	Open document diagnostics picker (LSP)	diagnostics_picker
D	Open workspace diagnostics picker (LSP)	workspace_diagnostics_picker
r	Rename symbol (LSP)	rename_symbol
a	Apply code action (LSP)	code_action
h	Select symbol references (LSP)	select_references_to_symbol_under_cursor
'	Open last fuzzy picker	last_picker
w	Enter window mode	N/A
c	Comment/uncomment selections	toggle_comments
C	Block comment/uncomment selections	toggle_block_comments
Alt-c	Line comment/uncomment selections	toggle_line_comments
p	Paste system clipboard after selections	paste_clipboard_after
P	Paste system clipboard before selections	paste_clipboard_before
y	Yank selections to clipboard	yank_to_clipboard
Y	Yank main selection to clipboard	yank_main_selection_to_clipboard
R	Replace selections by clipboard contents	replace_selections_with_clipboard
/	Global search in workspace folder	global_search
?	Open command palette	command_palette
💡 Global search displays results in a fuzzy picker, use Space + ' to bring it back up after opening a file.

Popup
Displays documentation for item under cursor. Remapping currently not supported.

Key	Description
Ctrl-u	Scroll up
Ctrl-d	Scroll down
Completion Menu
Displays documentation for the selected completion item. Remapping currently not supported.

Key	Description
Shift-Tab, Ctrl-p, Up	Previous entry
Tab, Ctrl-n, Down	Next entry
Enter	Close menu and accept completion
Ctrl-c	Close menu and reject completion
Any other keypresses result in the completion being accepted.

Signature-help Popup
Displays the signature of the selected completion item. Remapping currently not supported.

Key	Description
Alt-p	Previous signature
Alt-n	Next signature
Unimpaired
These mappings are in the style of vim-unimpaired.

Key	Description	Command
]d	Go to next diagnostic (LSP)	goto_next_diag
[d	Go to previous diagnostic (LSP)	goto_prev_diag
]D	Go to last diagnostic in document (LSP)	goto_last_diag
[D	Go to first diagnostic in document (LSP)	goto_first_diag
]f	Go to next function (TS)	goto_next_function
[f	Go to previous function (TS)	goto_prev_function
]t	Go to next type definition (TS)	goto_next_class
[t	Go to previous type definition (TS)	goto_prev_class
]a	Go to next argument/parameter (TS)	goto_next_parameter
[a	Go to previous argument/parameter (TS)	goto_prev_parameter
]c	Go to next comment (TS)	goto_next_comment
[c	Go to previous comment (TS)	goto_prev_comment
]T	Go to next test (TS)	goto_next_test
[T	Go to previous test (TS)	goto_prev_test
]p	Go to next paragraph	goto_next_paragraph
[p	Go to previous paragraph	goto_prev_paragraph
]g	Go to next change	goto_next_change
[g	Go to previous change	goto_prev_change
]G	Go to last change	goto_last_change
[G	Go to first change	goto_first_change
]Space	Add newline below	add_newline_below
[Space	Add newline above	add_newline_above
Insert mode
Accessed by typing i in normal mode.

Insert mode bindings are minimal by default. Helix is designed to be a modal editor, and this is reflected in the user experience and internal mechanics. Changes to the text are only saved for undos when escaping from insert mode to normal mode.

💡 New users are strongly encouraged to learn the modal editing paradigm to get the smoothest experience.

Key	Description	Command
Escape	Switch to normal mode	normal_mode
Ctrl-s	Commit undo checkpoint	commit_undo_checkpoint
Ctrl-x	Autocomplete	completion
Ctrl-r	Insert a register content	insert_register
Ctrl-w, Alt-Backspace	Delete previous word	delete_word_backward
Alt-d, Alt-Delete	Delete next word	delete_word_forward
Ctrl-u	Delete to start of line	kill_to_line_start
Ctrl-k	Delete to end of line	kill_to_line_end
Ctrl-h, Backspace, Shift-Backspace	Delete previous char	delete_char_backward
Ctrl-d, Delete	Delete next char	delete_char_forward
Ctrl-j, Enter	Insert new line	insert_newline
These keys are not recommended, but are included for new users less familiar with modal editors.

Key	Description	Command
Up	Move to previous line	move_line_up
Down	Move to next line	move_line_down
Left	Backward a char	move_char_left
Right	Forward a char	move_char_right
PageUp	Move one page up	page_up
PageDown	Move one page down	page_down
Home	Move to line start	goto_line_start
End	Move to line end	goto_line_end_newline
As you become more comfortable with modal editing, you may want to disable some insert mode bindings. You can do this by editing your config.toml file.

[keys.insert]
up = "no_op"
down = "no_op"
left = "no_op"
right = "no_op"
pageup = "no_op"
pagedown = "no_op"
home = "no_op"
end = "no_op"
Select / extend mode
Accessed by typing v in normal mode.

Select mode echoes Normal mode, but changes any movements to extend selections rather than replace them. Goto motions are also changed to extend, so that vgl, for example, extends the selection to the end of the line.

Search is also affected. By default, n and N will remove the current selection and select the next instance of the search term. Toggling this mode before pressing n or N makes it possible to keep the current selection. Toggling it on and off during your iterative searching allows you to selectively add search terms to your selections.

Picker
Keys to use within picker. Remapping currently not supported. See the documentation page on pickers for more info. Prompt keybinds also work in pickers, except where they conflict with picker keybinds.

Key	Description
Shift-Tab, Up, Ctrl-p	Previous entry
Tab, Down, Ctrl-n	Next entry
PageUp, Ctrl-u	Page up
PageDown, Ctrl-d	Page down
Home	Go to first entry
End	Go to last entry
Enter	Open selected
Alt-Enter	Open selected in the background without closing the picker
Ctrl-s	Open horizontally
Ctrl-v	Open vertically
Ctrl-t	Toggle preview
Escape, Ctrl-c	Close picker
Prompt
Keys to use within prompt, Remapping currently not supported.

Key	Description
Escape, Ctrl-c	Close prompt
Alt-b, Ctrl-Left	Backward a word
Ctrl-b, Left	Backward a char
Alt-f, Ctrl-Right	Forward a word
Ctrl-f, Right	Forward a char
Ctrl-e, End	Move prompt end
Ctrl-a, Home	Move prompt start
Ctrl-w, Alt-Backspace, Ctrl-Backspace	Delete previous word
Alt-d, Alt-Delete, Ctrl-Delete	Delete next word
Ctrl-u	Delete to start of line
Ctrl-k	Delete to end of line
Backspace, Ctrl-h, Shift-Backspace	Delete previous char
Delete, Ctrl-d	Delete next char
Ctrl-s	Insert a word under doc cursor, may be changed to Ctrl-r Ctrl-w later
Ctrl-p, Up	Select previous history
Ctrl-n, Down	Select next history
Ctrl-r	Insert the content of the register selected by following input char
Tab	Select next completion item
BackTab	Select previous completion item
Enter	Open selected




Command line
Quoting
Flags
Expansions
Exceptions
The command line is used for executing typable commands like :write or :quit. Press : to activate the command line.

Typable commands optionally accept arguments. :write for example accepts an optional path to write the file contents. The command line also supports a quoting syntax for arguments, flags to modify command behaviors, and expansions - a way to insert values from the editor. Most commands support these features but some have custom parsing rules (see the exceptions below).

Quoting
By default, command arguments are split on tabs and space characters. :open README.md CHANGELOG.md for example should open two files, README.md and CHANGELOG.md. Arguments that contain spaces can be surrounded in single quotes (') or backticks (`) to prevent the space from separating the argument, like :open 'a b.txt'.

Double quotes may be used the same way, but double quotes expand their inner content. :echo "%{cursor_line}" for example may print 1 because of the expansion for the cursor_line variable. :echo '%{cursor_line}' though prints %{cursor_line} literally: content within single quotes or backticks is interpreted as-is.

On Unix systems the backslash character may be used to escape certain characters depending on where it is used. Within an argument which isn't surround in quotes, the backslash can be used to escape the space or tab characters: :open a\ b.txt is equivalent to :open 'a b.txt'. The backslash may also be used to escape quote characters (', `, ") or the percent token (%) when used at the beginning of an argument. :echo \%%sh{foo} for example prints %sh{foo} instead of invoking a foo shell command and :echo \"quote prints "quote. The backslash character is treated literally in any other situation on Unix systems and always on Windows: :echo \n always prints \n.

Flags
Command flags are optional switches that can be used to alter the behavior of a command. For example the :sort command accepts an optional --reverse (or -r for short) flag which causes the sort command to reverse the sorting direction. Typing the - character shows completions for the current command's flags, if any.

The -- flag specifies the end of flags. All arguments after -- are treated as positional arguments: :open -- -a.txt opens a file called -a.txt.

Expansions
Expansions are patterns that Helix recognizes and replaces within the command line. Helix recognizes anything starting with a percent token (%) as an expansion, for example %sh{echo hi!}. Expansions are particularly useful when used in commands like :echo or :noop for executing simple scripts. For example:

[keys.normal]
# Print the current line's git blame information to the statusline.
space.B = ":echo %sh{git blame -L %{cursor_line},+1 %{buffer_name}}"
Expansions take the form %[<kind>]<open><contents><close>. In %sh{echo hi!}, for example, the kind is sh - the shell expansion - and the contents are "echo hi!", with { and } acting as opening and closing delimiters. The following open/close characters are recognized as expansion delimiter pairs: (/), [/], {/} and </>. Plus the single characters ', " or | may be used instead: %{cursor_line} is equivalent to %<cursor_line>, %[cursor_line] or %|cursor_line|.

To escape a percent character instead of treating it as an expansion, use two percent characters consecutively. To execute a shell command like date -u +'%Y-%m-%d', double the percent characters: :echo %sh{date -u +'%%Y-%%m-%%d'}.

When no <kind> is provided, Helix will expand a variable. For example %{cursor_line} can be used as in argument to insert the line number. :echo %{cursor_line} for instance may print 1 to the statusline.

The following variables are supported:

Name	Description
cursor_line	The line number of the primary cursor in the currently focused document, starting at 1.
cursor_column	The column number of the primary cursor in the currently focused document, starting at 1. This is counted as the number of grapheme clusters from the start of the line rather than bytes or codepoints.
buffer_name	The relative path of the currently focused document. [scratch] is expanded instead for scratch buffers.
line_ending	A string containing the line ending of the currently focused document. For example on Unix systems this is usually a line-feed character (\n) but on Windows systems this may be a carriage-return plus a line-feed (\r\n). The line ending kind of the currently focused document can be inspected with the :line-ending command.
language	A string containing the language name of the currently focused document.
selection	A string containing the contents of the primary selection of the currently focused document.
selection_line_start	The line number of the start of the primary selection in the currently focused document, starting at 1.
selection_line_end	The line number of the end of the primary selection in the currently focused document, starting at 1.
Aside from editor variables, the following expansions may be used:

Unicode %u{..}. The contents may contain up to six hexadecimal numbers corresponding to a Unicode codepoint value. For example :echo %u{25CF} prints ● to the statusline.
Shell %sh{..}. The contents are passed to the configured shell command. For example :echo %sh{echo "20 * 5" | bc} may print 100 on the statusline on when using a shell with echo and the bc calculator installed. Shell expansions are evaluated recursively. %sh{echo '%{buffer_name}:%{cursor_line}'} for example executes a command like echo 'README.md:1': the variables within the %sh{..} expansion are evaluated before executing the shell command.
As mentioned above, double quotes can be used to surround arguments containing spaces but also support expansions within the quoted content unlike singe quotes or backticks. For example :echo "circle: %u{25CF}" prints circle: ● to the statusline while :echo 'circle: %u{25CF}' prints circle: %u{25CF}.

Note that expansions are only evaluated once the Enter key is pressed in command mode.

Exceptions
The following commands support expansions but otherwise pass the given argument directly to the shell program without interpreting quotes:

:insert-output
:append-output
:pipe
:pipe-to
:run-shell-command
For example executing :sh echo "%{buffer_name}:%{cursor_column}" would pass text like echo "README.md:1" as an argument to the shell program: the expansions are evaluated but not the quotes. As mentioned above, percent characters can be used in shell commands by doubling the percent character. To insert the output of a command like date -u +'%Y-%m-%d' use :insert-output date -u +'%%Y-%%m-%%d'.

The :set-option and :toggle-option commands use regular parsing for the first argument - the config option name - and parse the rest depending on the config option's type. :set-option interprets the second argument as a string for string config options and parses everything else as JSON.

:toggle-option's behavior depends on the JSON type of the config option supplied as the first argument:

Booleans: only the config option name should be provided. For example :toggle-option auto-format will flip the auto-format option.
Strings: the rest of the command line is parsed with regular quoting rules. For example :toggle-option indent-heuristic hybrid tree-sitter simple cycles through "hybrid", "tree-sitter" and "simple" values on each invocation of the command.
Numbers, arrays and objects: the rest of the command line is parsed as a stream of JSON values. For example :toggle-option rulers [81] [51, 73] cycles through [81] and [51, 73].
When providing multiple values to :toggle-option there should be no duplicates. :toggle-option indent-heuristic hybrid simple tree-sitter simple for example would only toggle between "hybrid" and "tree-sitter" values.

:lsp-workspace-command works similarly to :toggle-option. The first argument (if present) is parsed according to normal rules. The rest of the line is parsed as JSON values. Unlike :toggle-option, string arguments for a command must be quoted. For example :lsp-workspace-command lsp.Command "foo" "bar".



Commands
Typable commands
Static commands
Typable commands
Typable commands are used from command mode and may take arguments. Command mode can be activated by pressing :. The built-in typable commands are:

Name	Description
:quit, :q	Close the current view.
:quit!, :q!	Force close the current view, ignoring unsaved changes.
:open, :o, :edit, :e	Open a file from disk into the current view.
:buffer-close, :bc, :bclose	Close the current buffer.
:buffer-close!, :bc!, :bclose!	Close the current buffer forcefully, ignoring unsaved changes.
:buffer-close-others, :bco, :bcloseother	Close all buffers but the currently focused one.
:buffer-close-others!, :bco!, :bcloseother!	Force close all buffers but the currently focused one.
:buffer-close-all, :bca, :bcloseall	Close all buffers without quitting.
:buffer-close-all!, :bca!, :bcloseall!	Force close all buffers ignoring unsaved changes without quitting.
:buffer-next, :bn, :bnext	Goto next buffer.
:buffer-previous, :bp, :bprev	Goto previous buffer.
:write, :w	Write changes to disk. Accepts an optional path (:write some/path.txt)
:write!, :w!	Force write changes to disk creating necessary subdirectories. Accepts an optional path (:write! some/path.txt)
:write-buffer-close, :wbc	Write changes to disk and closes the buffer. Accepts an optional path (:write-buffer-close some/path.txt)
:write-buffer-close!, :wbc!	Force write changes to disk creating necessary subdirectories and closes the buffer. Accepts an optional path (:write-buffer-close! some/path.txt)
:new, :n	Create a new scratch buffer.
:format, :fmt	Format the file using an external formatter or language server.
:indent-style	Set the indentation style for editing. ('t' for tabs or 1-16 for number of spaces.)
:line-ending	Set the document's default line ending. Options: crlf, lf.
:earlier, :ear	Jump back to an earlier point in edit history. Accepts a number of steps or a time span.
:later, :lat	Jump to a later point in edit history. Accepts a number of steps or a time span.
:write-quit, :wq, :x	Write changes to disk and close the current view. Accepts an optional path (:wq some/path.txt)
:write-quit!, :wq!, :x!	Write changes to disk and close the current view forcefully. Accepts an optional path (:wq! some/path.txt)
:write-all, :wa	Write changes from all buffers to disk.
:write-all!, :wa!	Forcefully write changes from all buffers to disk creating necessary subdirectories.
:write-quit-all, :wqa, :xa	Write changes from all buffers to disk and close all views.
:write-quit-all!, :wqa!, :xa!	Write changes from all buffers to disk and close all views forcefully (ignoring unsaved changes).
:quit-all, :qa	Close all views.
:quit-all!, :qa!	Force close all views ignoring unsaved changes.
:cquit, :cq	Quit with exit code (default 1). Accepts an optional integer exit code (:cq 2).
:cquit!, :cq!	Force quit with exit code (default 1) ignoring unsaved changes. Accepts an optional integer exit code (:cq! 2).
:theme	Change the editor theme (show current theme if no name specified).
:yank-join	Yank joined selections. A separator can be provided as first argument. Default value is newline.
:clipboard-yank	Yank main selection into system clipboard.
:clipboard-yank-join	Yank joined selections into system clipboard. A separator can be provided as first argument. Default value is newline.
:primary-clipboard-yank	Yank main selection into system primary clipboard.
:primary-clipboard-yank-join	Yank joined selections into system primary clipboard. A separator can be provided as first argument. Default value is newline.
:clipboard-paste-after	Paste system clipboard after selections.
:clipboard-paste-before	Paste system clipboard before selections.
:clipboard-paste-replace	Replace selections with content of system clipboard.
:primary-clipboard-paste-after	Paste primary clipboard after selections.
:primary-clipboard-paste-before	Paste primary clipboard before selections.
:primary-clipboard-paste-replace	Replace selections with content of system primary clipboard.
:show-clipboard-provider	Show clipboard provider name in status bar.
:change-current-directory, :cd	Change the current working directory.
:show-directory, :pwd	Show the current working directory.
:encoding	Set encoding. Based on https://encoding.spec.whatwg.org.
:character-info, :char	Get info about the character under the primary cursor.
:reload, :rl	Discard changes and reload from the source file.
:reload-all, :rla	Discard changes and reload all documents from the source files.
:update, :u	Write changes only if the file has been modified.
:lsp-workspace-command	Open workspace command picker
:lsp-restart	Restarts the given language servers, or all language servers that are used by the current file if no arguments are supplied
:lsp-stop	Stops the given language servers, or all language servers that are used by the current file if no arguments are supplied
:tree-sitter-scopes	Display tree sitter scopes, primarily for theming and development.
:tree-sitter-highlight-name	Display name of tree-sitter highlight scope under the cursor.
:debug-start, :dbg	Start a debug session from a given template with given parameters.
:debug-remote, :dbg-tcp	Connect to a debug adapter by TCP address and start a debugging session from a given template with given parameters.
:debug-eval	Evaluate expression in current debug context.
:vsplit, :vs	Open the file in a vertical split.
:vsplit-new, :vnew	Open a scratch buffer in a vertical split.
:hsplit, :hs, :sp	Open the file in a horizontal split.
:hsplit-new, :hnew	Open a scratch buffer in a horizontal split.
:tutor	Open the tutorial.
:goto, :g	Goto line number.
:set-language, :lang	Set the language of current buffer (show current language if no value specified).
:set-option, :set	Set a config option at runtime.
For example to disable smart case search, use :set search.smart-case false.
:toggle-option, :toggle	Toggle a config option at runtime.
For example to toggle smart case search, use :toggle search.smart-case.
:get-option, :get	Get the current value of a config option.
:sort	Sort ranges in selection.
:reflow	Hard-wrap the current selection of lines to a given width.
:tree-sitter-subtree, :ts-subtree	Display the smallest tree-sitter subtree that spans the primary selection, primarily for debugging queries.
:config-reload	Refresh user config.
:config-open	Open the user config.toml file.
:config-open-workspace	Open the workspace config.toml file.
:log-open	Open the helix log file.
:insert-output	Run shell command, inserting output before each selection.
:append-output	Run shell command, appending output after each selection.
:pipe, :|	Pipe each selection to the shell command.
:pipe-to	Pipe each selection to the shell command, ignoring output.
:run-shell-command, :sh, :!	Run a shell command
:reset-diff-change, :diffget, :diffg	Reset the diff change at the cursor position.
:clear-register	Clear given register. If no argument is provided, clear all registers.
:redraw	Clear and re-render the whole UI
:move, :mv	Move the current buffer and its corresponding file to a different path
:yank-diagnostic	Yank diagnostic(s) under primary cursor to register, or clipboard by default
:read, :r	Load a file into buffer
:echo	Prints the given arguments to the statusline.
:noop	Does nothing.
Static Commands
Static commands take no arguments and can be bound to keys. Static commands can also be executed from the command picker (<space>?). The built-in static commands are:

Name	Description	Default keybinds
no_op	Do nothing	
move_char_left	Move left	normal: h, <left>, insert: <left>
move_char_right	Move right	normal: l, <right>, insert: <right>
move_line_up	Move up	normal: gk
move_line_down	Move down	normal: gj
move_visual_line_up	Move up	normal: k, <up>, insert: <up>
move_visual_line_down	Move down	normal: j, <down>, insert: <down>
extend_char_left	Extend left	select: h, <left>
extend_char_right	Extend right	select: l, <right>
extend_line_up	Extend up	select: gk
extend_line_down	Extend down	select: gj
extend_visual_line_up	Extend up	select: k, <up>
extend_visual_line_down	Extend down	select: j, <down>
copy_selection_on_next_line	Copy selection on next line	normal: C, select: C
copy_selection_on_prev_line	Copy selection on previous line	normal: <A-C>, select: <A-C>
move_next_word_start	Move to start of next word	normal: w
move_prev_word_start	Move to start of previous word	normal: b
move_next_word_end	Move to end of next word	normal: e
move_prev_word_end	Move to end of previous word	
move_next_long_word_start	Move to start of next long word	normal: W
move_prev_long_word_start	Move to start of previous long word	normal: B
move_next_long_word_end	Move to end of next long word	normal: E
move_prev_long_word_end	Move to end of previous long word	
move_next_sub_word_start	Move to start of next sub word	
move_prev_sub_word_start	Move to start of previous sub word	
move_next_sub_word_end	Move to end of next sub word	
move_prev_sub_word_end	Move to end of previous sub word	
move_parent_node_end	Move to end of the parent node	normal: <A-e>
move_parent_node_start	Move to beginning of the parent node	normal: <A-b>
extend_next_word_start	Extend to start of next word	select: w
extend_prev_word_start	Extend to start of previous word	select: b
extend_next_word_end	Extend to end of next word	select: e
extend_prev_word_end	Extend to end of previous word	
extend_next_long_word_start	Extend to start of next long word	select: W
extend_prev_long_word_start	Extend to start of previous long word	select: B
extend_next_long_word_end	Extend to end of next long word	select: E
extend_prev_long_word_end	Extend to end of prev long word	
extend_next_sub_word_start	Extend to start of next sub word	
extend_prev_sub_word_start	Extend to start of previous sub word	
extend_next_sub_word_end	Extend to end of next sub word	
extend_prev_sub_word_end	Extend to end of prev sub word	
extend_parent_node_end	Extend to end of the parent node	select: <A-e>
extend_parent_node_start	Extend to beginning of the parent node	select: <A-b>
find_till_char	Move till next occurrence of char	normal: t
find_next_char	Move to next occurrence of char	normal: f
extend_till_char	Extend till next occurrence of char	select: t
extend_next_char	Extend to next occurrence of char	select: f
till_prev_char	Move till previous occurrence of char	normal: T
find_prev_char	Move to previous occurrence of char	normal: F
extend_till_prev_char	Extend till previous occurrence of char	select: T
extend_prev_char	Extend to previous occurrence of char	select: F
repeat_last_motion	Repeat last motion	normal: <A-.>, select: <A-.>
replace	Replace with new char	normal: r, select: r
switch_case	Switch (toggle) case	normal: ~, select: ~
switch_to_uppercase	Switch to uppercase	normal: <A-`>, select: <A-`>
switch_to_lowercase	Switch to lowercase	normal: `, select: `
page_up	Move page up	normal: <C-b>, Z<C-b>, z<C-b>, <pageup>, Z<pageup>, z<pageup>, select: <C-b>, Z<C-b>, z<C-b>, <pageup>, Z<pageup>, z<pageup>, insert: <pageup>
page_down	Move page down	normal: <C-f>, Z<C-f>, z<C-f>, <pagedown>, Z<pagedown>, z<pagedown>, select: <C-f>, Z<C-f>, z<C-f>, <pagedown>, Z<pagedown>, z<pagedown>, insert: <pagedown>
half_page_up	Move half page up	
half_page_down	Move half page down	
page_cursor_up	Move page and cursor up	
page_cursor_down	Move page and cursor down	
page_cursor_half_up	Move page and cursor half up	normal: <C-u>, Z<C-u>, z<C-u>, Z<backspace>, z<backspace>, select: <C-u>, Z<C-u>, z<C-u>, Z<backspace>, z<backspace>
page_cursor_half_down	Move page and cursor half down	normal: <C-d>, Z<C-d>, z<C-d>, Z<space>, z<space>, select: <C-d>, Z<C-d>, z<C-d>, Z<space>, z<space>
select_all	Select whole document	normal: %, select: %
select_regex	Select all regex matches inside selections	normal: s, select: s
split_selection	Split selections on regex matches	normal: S, select: S
split_selection_on_newline	Split selection on newlines	normal: <A-s>, select: <A-s>
merge_selections	Merge selections	normal: <A-minus>, select: <A-minus>
merge_consecutive_selections	Merge consecutive selections	normal: <A-_>, select: <A-_>
search	Search for regex pattern	normal: /, Z/, z/, select: /, Z/, z/
rsearch	Reverse search for regex pattern	normal: ?, Z?, z?, select: ?, Z?, z?
search_next	Select next search match	normal: n, Zn, zn, select: Zn, zn
search_prev	Select previous search match	normal: N, ZN, zN, select: ZN, zN
extend_search_next	Add next search match to selection	select: n
extend_search_prev	Add previous search match to selection	select: N
search_selection	Use current selection as search pattern	normal: <A-*>, select: <A-*>
search_selection_detect_word_boundaries	Use current selection as the search pattern, automatically wrapping with \b on word boundaries	normal: *, select: *
make_search_word_bounded	Modify current search to make it word bounded	
global_search	Global search in workspace folder	normal: <space>/, select: <space>/
extend_line	Select current line, if already selected, extend to another line based on the anchor	
extend_line_below	Select current line, if already selected, extend to next line	normal: x, select: x
extend_line_above	Select current line, if already selected, extend to previous line	
select_line_above	Select current line, if already selected, extend or shrink line above based on the anchor	
select_line_below	Select current line, if already selected, extend or shrink line below based on the anchor	
extend_to_line_bounds	Extend selection to line bounds	normal: X, select: X
shrink_to_line_bounds	Shrink selection to line bounds	normal: <A-x>, select: <A-x>
delete_selection	Delete selection	normal: d, select: d
delete_selection_noyank	Delete selection without yanking	normal: <A-d>, select: <A-d>
change_selection	Change selection	normal: c, select: c
change_selection_noyank	Change selection without yanking	normal: <A-c>, select: <A-c>
collapse_selection	Collapse selection into single cursor	normal: ;, select: ;
flip_selections	Flip selection cursor and anchor	normal: <A-;>, select: <A-;>
ensure_selections_forward	Ensure all selections face forward	normal: <A-:>, select: <A-:>
insert_mode	Insert before selection	normal: i, select: i
append_mode	Append after selection	normal: a, select: a
command_mode	Enter command mode	normal: :, select: :
file_picker	Open file picker	normal: <space>f, select: <space>f
file_picker_in_current_buffer_directory	Open file picker at current buffer's directory	
file_picker_in_current_directory	Open file picker at current working directory	normal: <space>F, select: <space>F
file_explorer	Open file explorer in workspace root	normal: <space>e, select: <space>e
file_explorer_in_current_buffer_directory	Open file explorer at current buffer's directory	normal: <space>E, select: <space>E
file_explorer_in_current_directory	Open file explorer at current working directory	
code_action	Perform code action	normal: <space>a, select: <space>a
buffer_picker	Open buffer picker	normal: <space>b, select: <space>b
jumplist_picker	Open jumplist picker	normal: <space>j, select: <space>j
symbol_picker	Open symbol picker	normal: <space>s, select: <space>s
changed_file_picker	Open changed file picker	normal: <space>g, select: <space>g
select_references_to_symbol_under_cursor	Select symbol references	normal: <space>h, select: <space>h
workspace_symbol_picker	Open workspace symbol picker	normal: <space>S, select: <space>S
diagnostics_picker	Open diagnostic picker	normal: <space>d, select: <space>d
workspace_diagnostics_picker	Open workspace diagnostic picker	normal: <space>D, select: <space>D
last_picker	Open last picker	normal: <space>', select: <space>'
insert_at_line_start	Insert at start of line	normal: I, select: I
insert_at_line_end	Insert at end of line	normal: A, select: A
open_below	Open new line below selection	normal: o, select: o
open_above	Open new line above selection	normal: O, select: O
normal_mode	Enter normal mode	normal: <esc>, select: v, insert: <esc>
select_mode	Enter selection extend mode	normal: v
exit_select_mode	Exit selection mode	select: <esc>
goto_definition	Goto definition	normal: gd, select: gd
goto_declaration	Goto declaration	normal: gD, select: gD
add_newline_above	Add newline above	normal: [<space>, select: [<space>
add_newline_below	Add newline below	normal: ]<space>, select: ]<space>
goto_type_definition	Goto type definition	normal: gy, select: gy
goto_implementation	Goto implementation	normal: gi, select: gi
goto_file_start	Goto line number else file start	normal: gg
goto_file_end	Goto file end	
extend_to_file_start	Extend to line number else file start	select: gg
extend_to_file_end	Extend to file end	
goto_file	Goto files/URLs in selections	normal: gf, select: gf
goto_file_hsplit	Goto files in selections (hsplit)	normal: <C-w>f, <space>wf, select: <C-w>f, <space>wf
goto_file_vsplit	Goto files in selections (vsplit)	normal: <C-w>F, <space>wF, select: <C-w>F, <space>wF
goto_reference	Goto references	normal: gr, select: gr
goto_window_top	Goto window top	normal: gt, select: gt
goto_window_center	Goto window center	normal: gc, select: gc
goto_window_bottom	Goto window bottom	normal: gb, select: gb
goto_last_accessed_file	Goto last accessed file	normal: ga, select: ga
goto_last_modified_file	Goto last modified file	normal: gm, select: gm
goto_last_modification	Goto last modification	normal: g., select: g.
goto_line	Goto line	normal: G, select: G
goto_last_line	Goto last line	normal: ge
extend_to_last_line	Extend to last line	select: ge
goto_first_diag	Goto first diagnostic	normal: [D, select: [D
goto_last_diag	Goto last diagnostic	normal: ]D, select: ]D
goto_next_diag	Goto next diagnostic	normal: ]d, select: ]d
goto_prev_diag	Goto previous diagnostic	normal: [d, select: [d
goto_next_change	Goto next change	normal: ]g, select: ]g
goto_prev_change	Goto previous change	normal: [g, select: [g
goto_first_change	Goto first change	normal: [G, select: [G
goto_last_change	Goto last change	normal: ]G, select: ]G
goto_line_start	Goto line start	normal: gh, <home>, select: gh, insert: <home>
goto_line_end	Goto line end	normal: gl, <end>, select: gl
goto_column	Goto column	normal: g|
extend_to_column	Extend to column	select: g|
goto_next_buffer	Goto next buffer	normal: gn, select: gn
goto_previous_buffer	Goto previous buffer	normal: gp, select: gp
goto_line_end_newline	Goto newline at line end	insert: <end>
goto_first_nonwhitespace	Goto first non-blank in line	normal: gs, select: gs
trim_selections	Trim whitespace from selections	normal: _, select: _
extend_to_line_start	Extend to line start	select: <home>
extend_to_first_nonwhitespace	Extend to first non-blank in line	
extend_to_line_end	Extend to line end	select: <end>
extend_to_line_end_newline	Extend to line end	
signature_help	Show signature help	
smart_tab	Insert tab if all cursors have all whitespace to their left; otherwise, run a separate command.	insert: <tab>
insert_tab	Insert tab char	insert: <S-tab>
insert_newline	Insert newline char	insert: <C-j>, <ret>
delete_char_backward	Delete previous char	insert: <C-h>, <backspace>, <S-backspace>
delete_char_forward	Delete next char	insert: <C-d>, <del>
delete_word_backward	Delete previous word	insert: <C-w>, <A-backspace>
delete_word_forward	Delete next word	insert: <A-d>, <A-del>
kill_to_line_start	Delete till start of line	insert: <C-u>
kill_to_line_end	Delete till end of line	insert: <C-k>
undo	Undo change	normal: u, select: u
redo	Redo change	normal: U, select: U
earlier	Move backward in history	normal: <A-u>, select: <A-u>
later	Move forward in history	normal: <A-U>, select: <A-U>
commit_undo_checkpoint	Commit changes to new checkpoint	insert: <C-s>
yank	Yank selection	normal: y, select: y
yank_to_clipboard	Yank selections to clipboard	normal: <space>y, select: <space>y
yank_to_primary_clipboard	Yank selections to primary clipboard	
yank_joined	Join and yank selections	
yank_joined_to_clipboard	Join and yank selections to clipboard	
yank_main_selection_to_clipboard	Yank main selection to clipboard	normal: <space>Y, select: <space>Y
yank_joined_to_primary_clipboard	Join and yank selections to primary clipboard	
yank_main_selection_to_primary_clipboard	Yank main selection to primary clipboard	
replace_with_yanked	Replace with yanked text	normal: R, select: R
replace_selections_with_clipboard	Replace selections by clipboard content	normal: <space>R, select: <space>R
replace_selections_with_primary_clipboard	Replace selections by primary clipboard	
paste_after	Paste after selection	normal: p, select: p
paste_before	Paste before selection	normal: P, select: P
paste_clipboard_after	Paste clipboard after selections	normal: <space>p, select: <space>p
paste_clipboard_before	Paste clipboard before selections	normal: <space>P, select: <space>P
paste_primary_clipboard_after	Paste primary clipboard after selections	
paste_primary_clipboard_before	Paste primary clipboard before selections	
indent	Indent selection	normal: <gt>, select: <gt>
unindent	Unindent selection	normal: <lt>, select: <lt>
format_selections	Format selection	normal: =, select: =
join_selections	Join lines inside selection	normal: J, select: J
join_selections_space	Join lines inside selection and select spaces	normal: <A-J>, select: <A-J>
keep_selections	Keep selections matching regex	normal: K, select: K
remove_selections	Remove selections matching regex	normal: <A-K>, select: <A-K>
align_selections	Align selections in column	normal: &, select: &
keep_primary_selection	Keep primary selection	normal: ,, select: ,
remove_primary_selection	Remove primary selection	normal: <A-,>, select: <A-,>
completion	Invoke completion popup	insert: <C-x>
hover	Show docs for item under cursor	normal: <space>k, select: <space>k
toggle_comments	Comment/uncomment selections	normal: <C-c>, <space>c, select: <C-c>, <space>c
toggle_line_comments	Line comment/uncomment selections	normal: <space><A-c>, select: <space><A-c>
toggle_block_comments	Block comment/uncomment selections	normal: <space>C, select: <space>C
rotate_selections_forward	Rotate selections forward	normal: ), select: )
rotate_selections_backward	Rotate selections backward	normal: (, select: (
rotate_selection_contents_forward	Rotate selection contents forward	normal: <A-)>, select: <A-)>
rotate_selection_contents_backward	Rotate selections contents backward	normal: <A-(>, select: <A-(>
reverse_selection_contents	Reverse selections contents	
expand_selection	Expand selection to parent syntax node	normal: <A-o>, <A-up>, select: <A-o>, <A-up>
shrink_selection	Shrink selection to previously expanded syntax node	normal: <A-i>, <A-down>, select: <A-i>, <A-down>
select_next_sibling	Select next sibling in the syntax tree	normal: <A-n>, <A-right>, select: <A-n>, <A-right>
select_prev_sibling	Select previous sibling the in syntax tree	normal: <A-p>, <A-left>, select: <A-p>, <A-left>
select_all_siblings	Select all siblings of the current node	normal: <A-a>, select: <A-a>
select_all_children	Select all children of the current node	normal: <A-I>, <S-A-down>, select: <A-I>, <S-A-down>
jump_forward	Jump forward on jumplist	normal: <C-i>, <tab>, select: <C-i>, <tab>
jump_backward	Jump backward on jumplist	normal: <C-o>, select: <C-o>
save_selection	Save current selection to jumplist	normal: <C-s>, select: <C-s>
jump_view_right	Jump to right split	normal: <C-w>l, <space>wl, <C-w><C-l>, <C-w><right>, <space>w<C-l>, <space>w<right>, select: <C-w>l, <space>wl, <C-w><C-l>, <C-w><right>, <space>w<C-l>, <space>w<right>
jump_view_left	Jump to left split	normal: <C-w>h, <space>wh, <C-w><C-h>, <C-w><left>, <space>w<C-h>, <space>w<left>, select: <C-w>h, <space>wh, <C-w><C-h>, <C-w><left>, <space>w<C-h>, <space>w<left>
jump_view_up	Jump to split above	normal: <C-w>k, <C-w><up>, <space>wk, <C-w><C-k>, <space>w<up>, <space>w<C-k>, select: <C-w>k, <C-w><up>, <space>wk, <C-w><C-k>, <space>w<up>, <space>w<C-k>
jump_view_down	Jump to split below	normal: <C-w>j, <space>wj, <C-w><C-j>, <C-w><down>, <space>w<C-j>, <space>w<down>, select: <C-w>j, <space>wj, <C-w><C-j>, <C-w><down>, <space>w<C-j>, <space>w<down>
swap_view_right	Swap with right split	normal: <C-w>L, <space>wL, select: <C-w>L, <space>wL
swap_view_left	Swap with left split	normal: <C-w>H, <space>wH, select: <C-w>H, <space>wH
swap_view_up	Swap with split above	normal: <C-w>K, <space>wK, select: <C-w>K, <space>wK
swap_view_down	Swap with split below	normal: <C-w>J, <space>wJ, select: <C-w>J, <space>wJ
transpose_view	Transpose splits	normal: <C-w>t, <space>wt, <C-w><C-t>, <space>w<C-t>, select: <C-w>t, <space>wt, <C-w><C-t>, <space>w<C-t>
rotate_view	Goto next window	normal: <C-w>w, <space>ww, <C-w><C-w>, <space>w<C-w>, select: <C-w>w, <space>ww, <C-w><C-w>, <space>w<C-w>
rotate_view_reverse	Goto previous window	
hsplit	Horizontal bottom split	normal: <C-w>s, <space>ws, <C-w><C-s>, <space>w<C-s>, select: <C-w>s, <space>ws, <C-w><C-s>, <space>w<C-s>
hsplit_new	Horizontal bottom split scratch buffer	normal: <C-w>ns, <space>wns, <C-w>n<C-s>, <space>wn<C-s>, select: <C-w>ns, <space>wns, <C-w>n<C-s>, <space>wn<C-s>
vsplit	Vertical right split	normal: <C-w>v, <space>wv, <C-w><C-v>, <space>w<C-v>, select: <C-w>v, <space>wv, <C-w><C-v>, <space>w<C-v>
vsplit_new	Vertical right split scratch buffer	normal: <C-w>nv, <space>wnv, <C-w>n<C-v>, <space>wn<C-v>, select: <C-w>nv, <space>wnv, <C-w>n<C-v>, <space>wn<C-v>
wclose	Close window	normal: <C-w>q, <space>wq, <C-w><C-q>, <space>w<C-q>, select: <C-w>q, <space>wq, <C-w><C-q>, <space>w<C-q>
wonly	Close windows except current	normal: <C-w>o, <space>wo, <C-w><C-o>, <space>w<C-o>, select: <C-w>o, <space>wo, <C-w><C-o>, <space>w<C-o>
select_register	Select register	normal: ", select: "
insert_register	Insert register	insert: <C-r>
copy_between_registers	Copy between two registers	
align_view_middle	Align view middle	normal: Zm, zm, select: Zm, zm
align_view_top	Align view top	normal: Zt, zt, select: Zt, zt
align_view_center	Align view center	normal: Zc, Zz, zc, zz, select: Zc, Zz, zc, zz
align_view_bottom	Align view bottom	normal: Zb, zb, select: Zb, zb
scroll_up	Scroll view up	normal: Zk, zk, Z<up>, z<up>, select: Zk, zk, Z<up>, z<up>
scroll_down	Scroll view down	normal: Zj, zj, Z<down>, z<down>, select: Zj, zj, Z<down>, z<down>
match_brackets	Goto matching bracket	normal: mm, select: mm
surround_add	Surround add	normal: ms, select: ms
surround_replace	Surround replace	normal: mr, select: mr
surround_delete	Surround delete	normal: md, select: md
select_textobject_around	Select around object	normal: ma, select: ma
select_textobject_inner	Select inside object	normal: mi, select: mi
goto_next_function	Goto next function	normal: ]f, select: ]f
goto_prev_function	Goto previous function	normal: [f, select: [f
goto_next_class	Goto next type definition	normal: ]t, select: ]t
goto_prev_class	Goto previous type definition	normal: [t, select: [t
goto_next_parameter	Goto next parameter	normal: ]a, select: ]a
goto_prev_parameter	Goto previous parameter	normal: [a, select: [a
goto_next_comment	Goto next comment	normal: ]c, select: ]c
goto_prev_comment	Goto previous comment	normal: [c, select: [c
goto_next_test	Goto next test	normal: ]T, select: ]T
goto_prev_test	Goto previous test	normal: [T, select: [T
goto_next_entry	Goto next pairing	normal: ]e, select: ]e
goto_prev_entry	Goto previous pairing	normal: [e, select: [e
goto_next_paragraph	Goto next paragraph	normal: ]p, select: ]p
goto_prev_paragraph	Goto previous paragraph	normal: [p, select: [p
dap_launch	Launch debug target	normal: <space>Gl, select: <space>Gl
dap_restart	Restart debugging session	normal: <space>Gr, select: <space>Gr
dap_toggle_breakpoint	Toggle breakpoint	normal: <space>Gb, select: <space>Gb
dap_continue	Continue program execution	normal: <space>Gc, select: <space>Gc
dap_pause	Pause program execution	normal: <space>Gh, select: <space>Gh
dap_step_in	Step in	normal: <space>Gi, select: <space>Gi
dap_step_out	Step out	normal: <space>Go, select: <space>Go
dap_next	Step to next	normal: <space>Gn, select: <space>Gn
dap_variables	List variables	normal: <space>Gv, select: <space>Gv
dap_terminate	End debug session	normal: <space>Gt, select: <space>Gt
dap_edit_condition	Edit breakpoint condition on current line	normal: <space>G<C-c>, select: <space>G<C-c>
dap_edit_log	Edit breakpoint log message on current line	normal: <space>G<C-l>, select: <space>G<C-l>
dap_switch_thread	Switch current thread	normal: <space>Gst, select: <space>Gst
dap_switch_stack_frame	Switch stack frame	normal: <space>Gsf, select: <space>Gsf
dap_enable_exceptions	Enable exception breakpoints	normal: <space>Ge, select: <space>Ge
dap_disable_exceptions	Disable exception breakpoints	normal: <space>GE, select: <space>GE
shell_pipe	Pipe selections through shell command	normal: |, select: |
shell_pipe_to	Pipe selections into shell command ignoring output	normal: <A-|>, select: <A-|>
shell_insert_output	Insert shell command output before selections	normal: !, select: !
shell_append_output	Append shell command output after selections	normal: <A-!>, select: <A-!>
shell_keep_pipe	Filter selections with shell predicate	normal: $, select: $
suspend	Suspend and return to shell	normal: <C-z>, select: <C-z>
rename_symbol	Rename symbol	normal: <space>r, select: <space>r
increment	Increment item under cursor	normal: <C-a>, select: <C-a>
decrement	Decrement item under cursor	normal: <C-x>, select: <C-x>
record_macro	Record macro	normal: Q, select: Q
replay_macro	Replay macro	normal: q, select: q
command_palette	Open command palette	normal: <space>?, select: <space>?
goto_word	Jump to a two-character label	normal: gw
extend_to_word	Extend to a two-character label	select: gw
goto_next_tabstop	Goto next snippet placeholder	
goto_prev_tabstop	Goto next snippet placeholder	
rotate_selections_first	Make the first selection your primary one	
rotate_selections_last	Make the last selection your primary one
