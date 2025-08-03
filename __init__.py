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
        # The value from a forced input is often a list, so we take the first element.
        return (str(value[0]),)

class InputText:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "text": ("STRING", {"multiline": True, "default": ""}),
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "get_text"
    CATEGORY = "MyCustomNodes"

    def get_text(self, text):
        return (text,)

class ShowText:

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "text": ("STRING", {"forceInput": True}),
            }
        }


    RETURN_TYPES = ()
    FUNCTION = "show"
    OUTPUT_NODE = True
    CATEGORY = "MyCustomNodes"

    def show(self, text):
        # Der Input ist meist eine Liste, daher zusammenfügen
        text_to_display = "\n".join(text)
        # Rückgabe als UI-Output, damit der Text im Node angezeigt wird
        return {"ui": {"text": [text_to_display]}}

NODE_CLASS_MAPPINGS = {
    "AddNumbers": AddNumbers,
    "FloatToStr": FloatToStr,
    "ShowText": ShowText,
    "InputText": InputText
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "AddNumbers": "Add Numbers",
    "FloatToStr": "Float to String",
    "ShowText": "Show Text",
    "InputText": "Input Text"
}