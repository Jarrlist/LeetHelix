import ast

user_code = """
data = [
    { "rank": 1,   "word": "a",    "count": 2565 },
    { "rank": 2,   "word": "and",  "count": 1777 },
    { "rank": 3,   "word": "of",   "count": 1331 },
    { "rank": 4,   "word": "that", "count": 1263 },
    { "rank": 5,   "word": "to",   "count": 1030 },
    { "rank": 6,   "word": "in",   "count": 1027 },
    { "rank": 7,   "word": "it",   "count": 754 },
    { "rank": 8,   "word": "as",   "count": 730 },
    { "rank": 9,   "word": "was",  "count": 687 },
    { "rank": 10,  "word": "you",  "count": 652 },
    { "rank": 11,  "word": "for",  "count": 630 },
]
"""

goal_code = """
data = [
    { "rank":  1, "word": "a",    "count": 2565 },
    { "rank":  2, "word": "and",  "count": 1777 },
    { "rank":  3, "word": "of",   "count": 1331 },
    { "rank":  4, "word": "that", "count": 1263 },
    { "rank":  5, "word": "to",   "count": 1030 },
    { "rank":  6, "word": "in",   "count": 1027 },
    { "rank":  7, "word": "it",   "count": 754 },
    { "rank":  8, "word": "as",   "count": 730 },
    { "rank":  9, "word": "was",  "count": 687 },
    { "rank": 10, "word": "you",  "count": 652 },
    { "rank": 11, "word": "for",  "count": 630 },
]
"""

def check_ast(u, g):
    try:
        u_ast = ast.parse(u)
        g_ast = ast.parse(g)
        dump_u = ast.dump(u_ast)
        dump_g = ast.dump(g_ast)
        match = dump_u == dump_g
        print(f"Match: {match}")
        if not match:
            print("Diff in AST dump:")
            # Simple diff of strings
            import difflib
            for line in difflib.unified_diff(dump_u.splitlines(), dump_g.splitlines()):
                print(line)
    except Exception as e:
        print(f"Error: {e}")

check_ast(user_code, goal_code)
