from typing import List, Dict


class Schema:
    def __init__(self, schema: Dict):
        self.schema = schema

    def validate(self, data: List[Dict]) -> bool:
        for entry in data:
            for key, value_type in self.schema.items():
                if key not in entry or not isinstance(entry[key], value_type):
                    raise ValueError(f"Invalid data format for key '{key}'")
        return True
