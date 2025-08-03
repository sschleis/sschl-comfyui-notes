class ShowText:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                # This is the data input socket. It has no widget of its own.
                "text": ("STRING", {"forceInput": True}),
                # This defines the text box widget that will be visible on the node.
                "display_text": ("STRING", {"multiline": True, "default": "Result appears here", "dynamicPrompts": False}),
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "show"
    OUTPUT_NODE = True
    CATEGORY = "MyCustomNodes"

    def show(self, text, display_text):
        text_to_display = "\n".join(text)
        print(f"[ShowText] Displaying text: {text_to_display}")
        return {"ui": {"display_text": [text_to_display]}, "result": (text,)}