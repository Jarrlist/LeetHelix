class ConfigLoader:
    def __init__(self, filename):
        self.filename = filename
        self.config = {}

    def load(self):
        print(f"Loading {self.filename}")
        return self.config
