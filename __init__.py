
class AddNumbers:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "a": ("FLOAT", {"default": 0.0}),
                "b": ("FLOAT", {"default": 0.0}),
            }
        }

    RETURN_TYPES = ("FLOAT",)
    FUNCTION = "add"
    CATEGORY = "MyCustomNodes"

    def add(self, a, b):
        return (a + b,)

class FloatToStr:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "value": ("FLOAT", {"forceInput": True}),
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "convert"
    CATEGORY = "MyCustomNodes"

    def convert(self, value):
        return (str(value),)

class ShowText:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "text": ("STRING", {"forceInput": True}),
            },
        }

    RETURN_TYPES = ()
    FUNCTION = "show"
    OUTPUT_NODE = True
    CATEGORY = "MyCustomNodes"

    def show(self, text):
        return {"ui": {"text": [text]}}

NODE_CLASS_MAPPINGS = {
    "AddNumbers": AddNumbers,
    "FloatToStr": FloatToStr,
    "ShowText": ShowText
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "AddNumbers": "Add Numbers",
    "FloatToStr": "Float to String",
    "ShowText": "Show Text"
}
