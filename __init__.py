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

import sys

class ShowText:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "text": ("STRING", {"forceInput": True}),
            },
            "hidden": {
                "unique_id": "UNIQUE_ID",
                "extra_pnginfo": "EXTRA_PNGINFO",
            },
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "show"
    OUTPUT_NODE = True
    CATEGORY = "MyCustomNodes"

    def show(self, text, unique_id=None, extra_pnginfo=None):
        # Log the received text and its type to the console for debugging
        print(f'[ShowText] Received text: "{text}"', file=sys.stderr)
        print(f'[ShowText] Type of text: {type(text)}', file=sys.stderr)

        # Ensure the text is a list of strings for the UI
        if isinstance(text, str):
            text_to_display = [text]
        elif isinstance(text, (list, tuple)):
            text_to_display = [str(item) for item in text]
        else:
            text_to_display = [str(text)]

        # This part is key: it updates the widget value in the workflow data,
        # which is what makes the text appear in the node's text box.
        if unique_id is not None and extra_pnginfo is not None:
            workflow = extra_pnginfo[0].get("workflow")
            if workflow:
                node = next((x for x in workflow["nodes"] if str(x["id"]) == str(unique_id[0])), None)
                if node:
                    node["widgets_values"] = text_to_display

        return {"ui": {"text": text_to_display}, "result": (text,)}

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