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

NODE_CLASS_MAPPINGS = {
    "AddNumbers": AddNumbers
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "AddNumbers": "Add Numbers"
}