class CombineStrings:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "string_a": ("STRING", {"forceInput": True}),
                "string_b": ("STRING", {"forceInput": True}),
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "combine"
    CATEGORY = "MyCustomNodes"

    def combine(self, string_a, string_b):
        # The inputs are lists of strings, so we join them before combining.
        result = string_a + "\n" + string_b
        return (result,)