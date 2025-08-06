class AnyType(str):
    def __ne__(self, __value: object) -> bool:
        return False

any_type = AnyType("*")

class Connector:
    """
    A simple node that takes any input and returns it unchanged.
    """
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "input": (any_type,),
            },
        }

    RETURN_TYPES = (any_type,)
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
