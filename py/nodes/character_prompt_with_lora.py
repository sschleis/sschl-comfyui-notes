import folder_paths
from nodes import LoraLoader
from .utils import FlexibleOptionalInputType, any_type


class CharacterPromptWithLora:

    CHARACTER_DATA = {
        "LadyM": {
            "prompt": "Always describe the woman as being around 32 years old. describe her always with dark burgundy hair. Describe her pose in detail. Describe the perspective in detail. Write everything in one continuous piece of text. Describe her outfit in detail. Describe her body shape. Call the woman LadyM. Describe her eyes with brown color.  describe also the other persons. describe her facial expression. describe her as caucasian woman. ignore the logo. Add the text to the describtion. Always describe women as having an athletic, slim figure. describe her eyes in detail. ignore the tattoos. describe her with a light smile. ignore the smartphone.",
            "filename": "LadyM",
            "key_prompt": " Describe her always with a necklace with a small key on it. ",
            "ignore_text_prompt": "",
            "lora": "ZIB/ZIB_LadyM_ws.safetensors",
        },
        "LadyK": {
            "prompt": "Always describe the woman as being around 35 years old. describe her always with reddish brown hair. Describe her pose in detail. Describe the perspective in detail. Write everything in one continuous piece of text. Describe her outfit in detail. Describe her body shape. Call the woman LadyK. Describe her eyes with brown color.  describe also the other persons. describe her facial expression. describe her as caucasian woman. ignore the logo. Add the text to the describtion. Always describe women as having an athletic, slim figure. ignore the cigarette. describe her eyes in detail. ignore the tattoos. ignore the text. describe here with glasses. she wears glasses.",
            "filename": "LadyK",
            "key_prompt": " Describe her always with a necklace with a small key on it. ",
            "ignore_text_prompt": "",
            "lora": "",
        },
        "SG": {
            "prompt": "Always describe the woman as being around 25 years old. describe her always with blond hair. Describe her pose in detail. Describe the perspective in detail. Write everything in one continuous piece of text. Describe her outfit in detail. Describe her body shape. Call the woman SlaveGirl. describe also the other persons. describe her facial expression. describe her as caucasian woman. ignore the logo. Add the text to the describtion. Always describe women as having an athletic, slim figure. ignore the cigarette. describe her eyes in detail. ignore the tattoos. ignore the text.",
            "filename": "SG",
            "key_prompt": " Describe her always with a necklace with a small key on it. ",
            "ignore_text_prompt": "",
            "lora": "",
        },
        "Pet": {
            "prompt": "Always describe the woman as being around 25 years old. describe her always with black hair, styled as an undercut with one side shaved and the other side shoulder long. Describe her pose in detail. Describe the perspective in detail. Write everything in one continuous piece of text. Describe her outfit in detail. Describe her body shape. Call the woman SlaveGirl. describe also the other persons. describe her facial expression. describe her as caucasian woman. ignore the logo. Add the text to the describtion. Always describe women as having an athletic, slim figure. ignore the cigarette. describe her eyes in detail. ignore the tattoos. ignore the text.",
            "filename": "Pet",
            "key_prompt": " Describe her always with a necklace with a small key on it. ",
            "ignore_text_prompt": "",
            "lora": "",
        },
        "LadySam": {
            "prompt": "Always describe the woman as being around 25 years old. describe her always with curly black hair. Describe her pose in detail. Describe the perspective in detail. Write everything in one continuous piece of text. Describe her outfit in detail. Describe her body shape. Call the woman LadySam. Describe her eyes with brown color.  describe also the other persons. describe her facial expression. describe her as caucasian woman. ignore the logo. Add the text to the describtion. Always describe women as having an athletic, slim figure. describe her eyes in detail. ignore the tattoos. describe her with a light smile. ignore the smartphone.",
            "filename": "LadySam",
            "key_prompt": " Describe her always with a necklace with a small key on it. ",
            "ignore_text_prompt": "",
            "lora": "",
        },
    }

    @classmethod
    def INPUT_TYPES(cls):
        lora_list = ["None"] + folder_paths.get_filename_list("loras")
        return {
            "required": {
                "character": (list(cls.CHARACTER_DATA.keys()),),
                "with_key": ("BOOLEAN", {"default": False}),
                "ignore_text": ("BOOLEAN", {"default": False}),
                "model": ("MODEL",),
                "clip": ("CLIP",),
                "lora_strength": ("FLOAT", {"default": 1.0, "min": -2.0, "max": 2.0, "step": 0.01}),
            },
            "optional": FlexibleOptionalInputType(type=any_type, data={
                "extra_lora_1": (lora_list,),
                "extra_lora_strength_1": ("FLOAT", {"default": 1.0, "min": -2.0, "max": 2.0, "step": 0.01}),
            }),
        }

    RETURN_TYPES = ("MODEL", "CLIP", "STRING", "STRING")
    RETURN_NAMES = ("model", "clip", "prompt", "filename")
    FUNCTION = "generate"
    CATEGORY = "MyCustomNodes"

    def generate(self, character, with_key, ignore_text, model, clip, lora_strength, **kwargs):
        data = self.CHARACTER_DATA[character]
        prompt = data["prompt"]
        if with_key:
            prompt += data["key_prompt"]
        if ignore_text:
            prompt += data["ignore_text_prompt"]
        filename = data["filename"]

        lora_loader = LoraLoader()

        if data["lora"]:
            model, clip = lora_loader.load_lora(model, clip, data["lora"], lora_strength, lora_strength)

        i = 1
        while True:
            lora_key = f"extra_lora_{i}"
            str_key = f"extra_lora_strength_{i}"
            if lora_key not in kwargs:
                break
            extra_lora = kwargs[lora_key]
            str_val = kwargs.get(str_key, 1.0)
            if extra_lora != "None":
                model, clip = lora_loader.load_lora(model, clip, extra_lora, str_val, str_val)
            i += 1

        return (model, clip, prompt, filename)
