import re

from nodes import LoraLoaderModelOnly


class AnyType(str):
    def __ne__(self, __value):
        return False


any_type = AnyType("*")


class FlexibleOptionalInputType(dict):
    """Allows a node to accept an arbitrary, unknown-in-advance set of optional inputs
    (used here for the dynamically added manual lora rows)."""

    def __init__(self, type):
        self.type = type

    def __getitem__(self, key):
        return (self.type,)

    def __contains__(self, key):
        return True


class Krea2LoraUtil:
    CHARACTER_LORAS = {
        "No": None,
        "LadyM": "Krea2_char\\Merlandia_krea2_lora_v2.safetensors",
        "LadyK": "Krea2_char\\lokal_L4dyK_krea2_lora_v1.safetensors",
        "SlaveGirl": "Krea2_char\\Sl4veGirl_krea2_lora_v1.safetensors",
        "Pet": "Krea2_char\\lokal_P3t_krea2_lora_v2.safetensors",
        "LadySam": "Krea2_char\\L4dySam_krea2_lora_v1.safetensors",
        "Natascha": "Krea2_char\\N4tasha_krea2_lora_v1.safetensors",
        "LadyN": "Krea2_char\\L4dyN_krea2_lora_v1.safetensors",
    }

    CHARACTER_PROMPTS = {
        "No": "Describe this image in detail",
        "LadyM": "Always describe the woman as being around 32 years old. describe her always with dark burgundy hair. Describe her pose in detail. Describe the perspective in detail. Write everything in one continuous piece of text. Describe her outfit in detail. Describe her body shape. Call the woman LadyM. Describe her eyes with brown color.  describe also the other persons. describe her facial expression. describe her as caucasian woman. ignore the logo. Add the text to the describtion. Always describe women as having an athletic, slim figure. describe her eyes in detail. describe her with a light smile. ignore the smartphone.",
        "LadyK": "Always describe the woman as being around 35 years old. describe her always with reddish brown hair. Describe her pose in detail. Describe the perspective in detail. Write everything in one continuous piece of text. Describe her outfit in detail. Describe her body shape. Call the woman LadyK. Describe her eyes with brown color.  describe also the other persons. describe her facial expression. describe her as caucasian woman. ignore the logo. Add the text to the describtion. Always describe women as having an athletic, slim figure. ignore the cigarette. describe her eyes in detail.",
        "SlaveGirl": "Always describe the woman as being around 25 years old. describe her always with blond hair. Describe her pose in detail. Describe the perspective in detail. Write everything in one continuous piece of text. Describe her outfit in detail. Describe her body shape. Call the woman SlaveGirl. describe also the other persons. describe her facial expression. describe her as caucasian woman. ignore the logo. Add the text to the describtion. Always describe women as having an athletic, slim figure. ignore the cigarette. describe her eyes in detail.",
        "Pet": "Always describe the woman as being around 25 years old. describe her always with black hair, styled as an undercut with one side shaved and the other side shoulder long. Describe her pose in detail. Describe the perspective in detail. Write everything in one continuous piece of text. Describe her outfit in detail. Describe her body shape. Call the woman SlaveGirl. describe also the other persons. describe her facial expression. describe her as caucasian woman. ignore the logo. Add the text to the describtion. Always describe women as having an athletic, slim figure. ignore the cigarette. describe her eyes in detail.",
        "LadySam": "Always describe the woman as being around 25 years old. describe her always with curly black hair. Describe her pose in detail. Describe the perspective in detail. Write everything in one continuous piece of text. Describe her outfit in detail. Describe her body shape. Call the woman LadySam. Describe her eyes with brown color.  describe also the other persons. describe her facial expression. describe her as caucasian woman. ignore the logo. Add the text to the describtion. Always describe women as having an athletic, slim figure. describe her eyes in detail. describe her with a light smile. ignore the smartphone.",
        "Natascha": "Always describe the woman as being around 48 years old. describe her always with blond hair. Describe her pose in detail. Describe the perspective in detail. Write everything in one continuous piece of text. Describe her outfit in detail. Describe her body shape. Call the woman Natascha. Describe her eyes with blue color.  describe also the other persons. describe her facial expression. describe her as caucasian woman. ignore the logo. Add the text to the describtion. Always describe women as having an athletic, slim figure. describe her eyes in detail. describe her with a light smile. ignore the smartphone.",
        "LadyN": "Always describe the woman as being around 32 years old. describe her always with light ash brown hair. Describe her pose in detail. Describe the perspective in detail. Write everything in one continuous piece of text. Describe her outfit in detail. Describe her body shape. Call the woman LadyN. Describe her eyes with grey-blue color.  describe also the other persons. describe her facial expression. describe her as caucasian woman. ignore the logo. Add the text to the describtion. Always describe women as having an athletic, slim figure. describe her eyes in detail. ignore the tattoos. describe her with a light smile. ignore the smartphone.",
    }

    REALISTIC_LORAS = [
        ("krea2_real\\ultra_real_krea2_v1.safetensors", 1.00),
        ("krea2_real\\real_3d_krea2_loraholic.safetensors", 0.90),
        ("krea2_real\\skindetails_krea2_loraholic.safetensors", 0.60),
        ("krea2_style\\realism_engine_krea2_v2.safetensors", 0.80),
        ("krea2_real\\detail_slider_krea2_loraholic.safetensors", 0.80),
    ]

    KREA2_REALISM_V2_LORA = ("krea2_real\\Krea2-realism-V2.safetensors", 0.20)
    SNOFS_LORA = ("krea2_real\\snofs_krea_v1_1.safetensors", 0.80)

    NECKLACE_PROMPT = " Describe her with a nacklace with a tiny key on it"
    GLASSES_PROMPT = " Describe her with glasses"

    MANUAL_LORA_ENABLED_PATTERN = re.compile(r"^manual_lora_(\d+)_enabled$")

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "model": ("MODEL",),
                "character": (list(cls.CHARACTER_LORAS.keys()), {"default": "No"}),
                "with_necklace": ("BOOLEAN", {"default": False}),
                "with_glasses": ("BOOLEAN", {"default": False}),
                "lora_strength": ("FLOAT", {"default": 1.0, "min": -2.0, "max": 2.0, "step": 0.01}),
                "realistic": ("BOOLEAN", {"default": True}),
                "krea2_realism_v2": ("BOOLEAN", {"default": False}),
                "snofs": ("BOOLEAN", {"default": False}),
            },
            "optional": FlexibleOptionalInputType(any_type),
        }

    RETURN_TYPES = ("MODEL", "STRING", "STRING")
    RETURN_NAMES = ("model", "name", "prompt")
    FUNCTION = "process"
    CATEGORY = "MyCustomNodes"

    def process(self, model, character, with_necklace, with_glasses, lora_strength, realistic,
                krea2_realism_v2, snofs, **kwargs):
        lora_name = self.CHARACTER_LORAS[character]
        lora_loader = LoraLoaderModelOnly()

        if lora_name:
            model = lora_loader.load_lora_model_only(model, lora_name, lora_strength)[0]

        if realistic:
            for real_lora_name, real_lora_strength in self.REALISTIC_LORAS:
                model = lora_loader.load_lora_model_only(model, real_lora_name, real_lora_strength)[0]

        if krea2_realism_v2:
            lora_name_, strength_ = self.KREA2_REALISM_V2_LORA
            model = lora_loader.load_lora_model_only(model, lora_name_, strength_)[0]

        if snofs:
            lora_name_, strength_ = self.SNOFS_LORA
            model = lora_loader.load_lora_model_only(model, lora_name_, strength_)[0]

        row_indices = sorted(
            int(match.group(1))
            for key in kwargs
            if (match := self.MANUAL_LORA_ENABLED_PATTERN.match(key))
        )
        for i in row_indices:
            enabled = kwargs.get(f"manual_lora_{i}_enabled")
            manual_lora_name = kwargs.get(f"manual_lora_{i}_name")
            manual_lora_strength = kwargs.get(f"manual_lora_{i}_strength")
            if enabled and manual_lora_name and manual_lora_name != "None":
                model = lora_loader.load_lora_model_only(model, manual_lora_name, manual_lora_strength)[0]

        prompt = self.CHARACTER_PROMPTS[character]
        if with_necklace:
            prompt += self.NECKLACE_PROMPT
        if with_glasses:
            prompt += self.GLASSES_PROMPT

        return (model, character, prompt)
