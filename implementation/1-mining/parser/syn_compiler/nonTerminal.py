import json

class NonTerminal:

    def __init__(self):
        self.key = ""
        self.value = None

    def __str__(self) -> str:
        return json.dumps(self.value, indent=2)