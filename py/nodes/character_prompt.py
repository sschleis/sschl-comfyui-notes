class CharacterPrompt:

    KEY_PROMPT = " Describe her always with a necklace with a small key on it. "
    IGNORE_TEXT_PROMPT = "Ignore the text on the picture. "
    IGNORE_TATTOOS_PROMPT = "ignore the tattoos. "
    COLLAR_PROMPT = "Describe her always with a bold, high-polish metal collar featuring a seamless hinge and a lockable O-ring for a striking, industrial aesthetic around her neck. "
    GLASSES_PROMPT = "describe here with glasses. she wears glasses."

    CHARACTER_DATA = {
        "LadyM": {
            "prompt": "Always describe the woman as being around 32 years old. describe her always with dark burgundy hair. Describe her pose in detail. Describe the perspective in detail. Write everything in one continuous piece of text. Describe her outfit in detail. Describe her body shape. Call the woman LadyM. Describe her eyes with brown color.  describe also the other persons. describe her facial expression. describe her as caucasian woman. ignore the logo. Add the text to the describtion. Always describe women as having an athletic, slim figure. describe her eyes in detail. ignore the tattoos. describe her with a light smile. ignore the smartphone.",
            "filename": "LadyM",
        },
        "LadyM Office": {
            "prompt": "Always describe the woman as being around 30 years old. describe her always with dark burgundy hair. Describe the location as an modern IT-Office. She is walking. Write everything in one continuous piece of text. Describe her outfit in detail. Describe her body shape. Call the woman LadyM. Describe her eyes with brown color.  describe also the other persons. describe her facial expression. describe her as caucasian woman. ignore the logo. Always describe women as having an athletic, slim figure. ignore the cigarette. describe her eyes in detail. ignore the tattoos.",
            "filename": "LadyM",
        },
        "LadyM Random": {
            "prompt": "Describe the woman's outfit in detail, including her shoes. Also, always describe her as having dark burgundy hair. Ignore the background and pose, and come up with a random location and pose that matches the outfit. Ignore tattoos in your description. she is 32 years old.",
            "filename": "LadyM",
        },
        "LadyK": {
            "prompt": "Always describe the woman as being around 35 years old. describe her always with reddish brown hair. Describe her pose in detail. Describe the perspective in detail. Write everything in one continuous piece of text. Describe her outfit in detail. Describe her body shape. Call the woman LadyK. Describe her eyes with brown color.  describe also the other persons. describe her facial expression. describe her as caucasian woman. ignore the logo. Add the text to the describtion. Always describe women as having an athletic, slim figure. ignore the cigarette. describe her eyes in detail. ignore the tattoos. describe here with glasses. she wears glasses.",
            "filename": "LadyK",
        },
        "SG": {
            "prompt": "Always describe the woman as being around 25 years old. describe her always with blond hair. Describe her pose in detail. Describe the perspective in detail. Write everything in one continuous piece of text. Describe her outfit in detail. Describe her body shape. Call the woman SlaveGirl. describe also the other persons. describe her facial expression. describe her as caucasian woman. ignore the logo. Add the text to the describtion. Always describe women as having an athletic, slim figure. ignore the cigarette. describe her eyes in detail. ignore the tattoos.",
            "filename": "SG",
        },
        "Pet": {
            "prompt": "Always describe the woman as being around 25 years old. describe her always with black hair, styled as an undercut with one side shaved and the other side shoulder long. Describe her pose in detail. Describe the perspective in detail. Write everything in one continuous piece of text. Describe her outfit in detail. Describe her body shape. Call the woman SlaveGirl. describe also the other persons. describe her facial expression. describe her as caucasian woman. ignore the logo. Add the text to the describtion. Always describe women as having an athletic, slim figure. ignore the cigarette. describe her eyes in detail. ignore the tattoos.",
            "filename": "Pet",
        },
        "LadySam": {
            "prompt": "Always describe the woman as being around 25 years old. describe her always with curly black hair. Describe her pose in detail. Describe the perspective in detail. Write everything in one continuous piece of text. Describe her outfit in detail. Describe her body shape. Call the woman LadySam. Describe her eyes with brown color.  describe also the other persons. describe her facial expression. describe her as caucasian woman. ignore the logo. Add the text to the describtion. Always describe women as having an athletic, slim figure. describe her eyes in detail. ignore the tattoos. describe her with a light smile. ignore the smartphone.",
            "filename": "LadySam",
        },
        "LadyN": {
            "prompt": "Always describe the woman as being around 32 years old. describe her always with light ash brown hair. Describe her pose in detail. Describe the perspective in detail. Write everything in one continuous piece of text. Describe her outfit in detail. Describe her body shape. Call the woman LadyN. Describe her eyes with grey-blue color.  describe also the other persons. describe her facial expression. describe her as caucasian woman. ignore the logo. Add the text to the describtion. Always describe women as having an athletic, slim figure. describe her eyes in detail. ignore the tattoos. describe her with a light smile. ignore the smartphone.",
            "filename": "LadyN",
        },
    }

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "character": (list(cls.CHARACTER_DATA.keys()),),
                "with_key": ("BOOLEAN", {"default": False}),
                "with_glasses": ("BOOLEAN", {"default": False}),
                "with_collar": ("BOOLEAN", {"default": False}),
                "ignore_text": ("BOOLEAN", {"default": False}),
                "ignore_tattoos": ("BOOLEAN", {"default": False}),
            },
        }

    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("prompt", "filename")
    FUNCTION = "generate"
    CATEGORY = "MyCustomNodes"

    def generate(self, character, with_key=False, with_glasses=False, with_collar=False, ignore_text=False, ignore_tattoos=False):
        data = self.CHARACTER_DATA[character]
        prompt = data["prompt"]
        if with_key:
            prompt += self.KEY_PROMPT
        if with_glasses:
            prompt += self.GLASSES_PROMPT
        if with_collar:
            prompt += self.COLLAR_PROMPT
        if ignore_text:
            prompt += self.IGNORE_TEXT_PROMPT
        if ignore_tattoos:
            prompt += self.IGNORE_TATTOOS_PROMPT
        filename = data["filename"]
        return (prompt, filename)
