import json
from collections import defaultdict

# Создаем defaultdict с значением по умолчанию 0
class SimpleDatabase:
    def __init__(self, filename='database.json'):
        self.filename = filename
        self.data = self.load_data()

    def load_data(self):
        try:
            with open(self.filename, 'r') as file:
                data = defaultdict(int,json.load(file))
            return data
        except (FileNotFoundError, json.JSONDecodeError):
            return defaultdict(int)

    def save_data(self):
        with open(self.filename, 'w') as file:
            json.dump(self.data, file, indent=2)


