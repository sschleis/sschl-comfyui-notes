class Switch:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "use_input_1": ("BOOLEAN", {"default": True}),
                "use_input_2": ("BOOLEAN", {"default": False}),
                "use_input_3": ("BOOLEAN", {"default": False}),
                "use_input_4": ("BOOLEAN", {"default": False}),
                "use_input_5": ("BOOLEAN", {"default": False}),
            },
            "optional": {
                "input_1": ("STRING", {"forceInput": True}),
                "input_2": ("STRING", {"forceInput": True}),
                "input_3": ("STRING", {"forceInput": True}),
                "input_4": ("STRING", {"forceInput": True}),
                "input_5": ("STRING", {"forceInput": True}),
            },
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "select"
    CATEGORY = "MyCustomNodes"

    def select(
        self,
        use_input_1,
        use_input_2,
        use_input_3,
        use_input_4,
        use_input_5,
        **kwargs,
    ):
        selected = []
        for index, enabled in enumerate(
            [use_input_1, use_input_2, use_input_3, use_input_4, use_input_5], start=1
        ):
            if not enabled:
                continue

            value = kwargs.get(f"input_{index}")
            if value is not None and value != "":
                selected.append(value)

        return ("\n".join(selected),)
