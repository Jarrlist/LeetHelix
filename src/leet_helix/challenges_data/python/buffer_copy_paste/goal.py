# Copy the function 'parse_line' from parser_utils.py below this line
def parse_line(line):
    if not line:
        return None
    parts = line.split('=')
    if len(parts) != 2:
        return None
    return parts[0].strip(), parts[1].strip()

# Copy the class 'ConfigLoader' from config_loader.py below this line
class ConfigLoader:
    def __init__(self, filename):
        self.filename = filename
        self.config = {}

    def load(self):
        print(f"Loading {self.filename}")
        return self.config
