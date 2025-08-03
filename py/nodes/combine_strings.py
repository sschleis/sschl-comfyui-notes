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
        combined_string_a = "\n".join(string_a)
        combined_string_b = "\n".join(string_b)
        result = combined_string_a + combined_string_b
        return (result,)