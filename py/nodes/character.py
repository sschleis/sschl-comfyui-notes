import os
import csv

class Character:
    def __init__(self):
        self.characters = self.load_characters()

    def load_characters(self):
        characters = {}
        # Construct the absolute path to the CSV file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        csv_path = os.path.join(current_dir, "..", "data", "characters.csv")

        if not os.path.exists(csv_path):
            print(f"[Character Node] Error: characters.csv not found at {csv_path}")
            return {}

        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader)  # Skip header row
            for row in reader:
                if len(row) == 2:
                    name, description = row
                    characters[name] = description
        return characters

    @classmethod
    def INPUT_TYPES(s):
        # Load characters dynamically for the dropdown
        char_instance = s()
        character_names = list(char_instance.characters.keys())
        if not character_names:
            character_names = ["No Characters Found"]

        return {
            "required": {
                "character_name": (character_names, {"default": character_names[0]}),
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "get_description"
    CATEGORY = "MyCustomNodes"

    def get_description(self, character_name):
        description = self.characters.get(character_name, "Character not found.")
        return (description,)
