class GroupManager:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},
            "hidden": {"prompt": "PROMPT", "extra_pnginfo": "EXTRA_PNGINFO"},
        }

    RETURN_TYPES = ()
    FUNCTION = "do_nothing"
    CATEGORY = "sschl-comfyui-notes"
    OUTPUT_NODE = True

    def do_nothing(self, **kwargs):
        return {}

NODE_CLASS_MAPPINGS = {
    "GroupManager": GroupManager
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "GroupManager": "Group Manager"
}
