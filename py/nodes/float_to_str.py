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