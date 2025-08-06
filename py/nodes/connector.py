class Connector:
    """
    A simple node that takes any input and returns it unchanged.
    """
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "input": ("*",),
            },
        }

    RETURN_TYPES = ("*",)
    FUNCTION = "connect"

    CATEGORY = "sschl"

    def connect(self, input):
        return (input,)

NODE_CLASS_MAPPINGS = {
    "Connector": Connector
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Connector": "Connector"
}
