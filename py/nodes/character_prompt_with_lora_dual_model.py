import folder_paths
from nodes import LoraLoader


class CharacterPromptWithLoraWithDualModel:

    CHARACTER_DATA = {
        "LadyM": {
            "prompt": "Always describe the woman as being around 32 years old. describe her always with dark burgundy hair. Describe her pose in detail. Describe the perspective in detail. Write everything in one continuous piece of text. Describe her outfit in detail. Describe her body shape. Call the woman LadyM. Describe her eyes with brown color.  describe also the other persons. describe her facial expression. describe her as caucasian woman. ignore the logo. Add the text to the describtion. Always describe women as having an athletic, slim figure. describe her eyes in detail. ignore the tattoos. describe her with a light smile. ignore the smartphone.",
            "filename": "LadyM",
            "key_prompt": " Describe her always with a necklace with a small key on it. ",
            "ignore_text_prompt": "Ignore the text on the picture. ",
            "zib_lora": "ZIB\ZIB_LadyM_ws.safetensors",
            "zit_lora": "zit\LadyM_ZIT_epoch_10.safetensors",
        },
        "LadyK": {
            "prompt": "Always describe the woman as being around 35 years old. describe her always with reddish brown hair. Describe her pose in detail. Describe the perspective in detail. Write everything in one continuous piece of text. Describe her outfit in detail. Describe her body shape. Call the woman LadyK. Describe her eyes with brown color.  describe also the other persons. describe her facial expression. describe her as caucasian woman. ignore the logo. Add the text to the describtion. Always describe women as having an athletic, slim figure. ignore the cigarette. describe her eyes in detail. ignore the tattoos. ignore the text. describe here with glasses. she wears glasses.",
            "filename": "LadyK",
            "key_prompt": " Describe her always with a necklace with a small key on it. ",
            "ignore_text_prompt": "Ignore the text on the picture. ",
            "zib_lora": "ZIB\ZIB_LadyK_ws.safetensors",
            "zit_lora": "zit\LadyK_ZIT_epoch_10.safetensors",
        },
        "SG": {
            "prompt": "Always describe the woman as being around 25 years old. describe her always with blond hair. Describe her pose in detail. Describe the perspective in detail. Write everything in one continuous piece of text. Describe her outfit in detail. Describe her body shape. Call the woman SlaveGirl. describe also the other persons. describe her facial expression. describe her as caucasian woman. ignore the logo. Add the text to the describtion. Always describe women as having an athletic, slim figure. ignore the cigarette. describe her eyes in detail. ignore the tattoos. ignore the text.",
            "filename": "SG",
            "key_prompt": " Describe her always with a necklace with a small key on it. ",
            "ignore_text_prompt": "Ignore the text on the picture. ",
            "zib_lora": "ZIB\ZIB_SlaveGirl_ws.safetensors",
            "zit_lora": "zit\SlaveGirl_ZIT_epoch_10.safetensors",
        },
        "Pet": {
            "prompt": "Always describe the woman as being around 25 years old. describe her always with black hair, styled as an undercut with one side shaved and the other side shoulder long. Describe her pose in detail. Describe the perspective in detail. Write everything in one continuous piece of text. Describe her outfit in detail. Describe her body shape. Call the woman SlaveGirl. describe also the other persons. describe her facial expression. describe her as caucasian woman. ignore the logo. Add the text to the describtion. Always describe women as having an athletic, slim figure. ignore the cigarette. describe her eyes in detail. ignore the tattoos. ignore the text.",
            "filename": "Pet",
            "key_prompt": " Describe her always with a necklace with a small key on it. ",
            "ignore_text_prompt": "Ignore the text on the picture. ",
            "zib_lora": "ZIB\ZIB_PetGirl_ws.safetensors",
            "zit_lora": "zit\PetGirl_ZIT_epoch_10.safetensors",
        },
        "LadySam": {
            "prompt": "Always describe the woman as being around 25 years old. describe her always with curly black hair. Describe her pose in detail. Describe the perspective in detail. Write everything in one continuous piece of text. Describe her outfit in detail. Describe her body shape. Call the woman LadySam. Describe her eyes with brown color.  describe also the other persons. describe her facial expression. describe her as caucasian woman. ignore the logo. Add the text to the describtion. Always describe women as having an athletic, slim figure. describe her eyes in detail. ignore the tattoos. describe her with a light smile. ignore the smartphone.",
            "filename": "LadySam",
            "key_prompt": " Describe her always with a necklace with a small key on it. ",
            "ignore_text_prompt": "Ignore the text on the picture. ",
            "zib_lora": "ZIB\ZIB_LadySam.safetensors",
            "zit_lora": "zit\LadySam_ZIT_epoch_10.safetensors",
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
                "zib_model": ("MODEL",),
                "zib_clip": ("CLIP",),
                "zit_model": ("MODEL",),
                "extra_lora_1": (lora_list,),
                "extra_lora_strength_1": ("FLOAT", {"default": 1.0, "min": -2.0, "max": 2.0, "step": 0.01}),
                "extra_lora_2": (lora_list,),
                "extra_lora_strength_2": ("FLOAT", {"default": 1.0, "min": -2.0, "max": 2.0, "step": 0.01}),
                "extra_lora_3": (lora_list,),
                "extra_lora_strength_3": ("FLOAT", {"default": 1.0, "min": -2.0, "max": 2.0, "step": 0.01}),
            },
            "optional": {
                "zit_clip": ("CLIP",),
            },
        }

    RETURN_TYPES = ("MODEL", "CLIP", "MODEL", "CLIP", "STRING", "STRING")
    RETURN_NAMES = ("zib_model", "zib_clip", "zit_model", "zit_clip", "prompt", "filename")
    FUNCTION = "generate"
    CATEGORY = "MyCustomNodes"

    def generate(self, character, with_key, ignore_text, zib_model, zib_clip, zit_model, zit_clip=None,
                 extra_lora_1, extra_lora_strength_1,
                 extra_lora_2, extra_lora_strength_2,
                 extra_lora_3, extra_lora_strength_3):
        data = self.CHARACTER_DATA[character]
        prompt = data["prompt"]
        if with_key:
            prompt += data["key_prompt"]
        if ignore_text:
            prompt += data["ignore_text_prompt"]
        filename = data["filename"]

        zib_model, zib_clip = LoraLoader().load_lora(zib_model, zib_clip, "ZIB\Z-Image-Fun-Lora-Distill-8-Steps_ComfyUI.safetensors", 1.0, 1.0)

        if data["zib_lora"]:
            zib_model, zib_clip = LoraLoader().load_lora(zib_model, zib_clip, data["zib_lora"], 1.0, 1.0)

        if data["zit_lora"]:
            zit_model, zit_clip = LoraLoader().load_lora(zit_model, zit_clip, data["zit_lora"], 0.4, 0.4)

        for extra_lora, str_val in [
            (extra_lora_1, extra_lora_strength_1),
            (extra_lora_2, extra_lora_strength_2),
            (extra_lora_3, extra_lora_strength_3),
        ]:
            if extra_lora != "None":
                zib_model, zib_clip = LoraLoader().load_lora(zib_model, zib_clip, extra_lora, str_val, str_val)
                #zit_model, zit_clip = LoraLoader().load_lora(zit_model, zit_clip, extra_lora, str_val, str_val)

        return (zib_model, zib_clip, zit_model, zit_clip, prompt, filename)
