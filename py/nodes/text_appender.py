class TextAppender:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "text_in": ("STRING", {"forceInput": True}),
                "append_text": ("STRING", {"multiline": True, "default": ""}),
                "position": (["end", "start"],),
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "append"
    CATEGORY = "MyCustomNodes"

    def append(self, text_in, append_text, position):
        # Ensure text_in is a single string, as it might come as a list/tuple
        if isinstance(text_in, (list, tuple)):
            text_in = "\n".join(text_in)
        else:
            text_in = str(text_in)

        if position == "start":
            result = append_text + "\n" + text_in
        else:  # position == "end"
            result = text_in + "\n" + append_text

        return (result,)
