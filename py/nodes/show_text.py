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

    RETURN_TYPES = ()
    FUNCTION = "show"
    OUTPUT_NODE = True
    CATEGORY = "MyCustomNodes"

    def show(self, text, display_text):
        # The input from the socket is a list, so we join it into a single string.
        text_to_display = "\n".join(text)

        # This is the key: we return a UI dictionary telling ComfyUI to update
        # the 'display_text' widget with our formatted text.
        return {"ui": {"display_text": [text_to_display]}}