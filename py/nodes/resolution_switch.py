class ResolutionSwitch:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "use_first": ("BOOLEAN", {"default": True}),
                "x1": ("INT", {"default": 0, "min": 0, "max": 8192}),
                "y1": ("INT", {"default": 0, "min": 0, "max": 8192}),
                "x2": ("INT", {"default": 0, "min": 0, "max": 8192}),
                "y2": ("INT", {"default": 0, "min": 0, "max": 8192}),
            }
        }

    RETURN_TYPES = ("INT", "INT")
    RETURN_NAMES = ("x", "y")
    FUNCTION = "switch"
    CATEGORY = "MyCustomNodes"

    def switch(self, use_first, x1, y1, x2, y2):
        if use_first:
            return (x1, y1)
        return (x2, y2)
