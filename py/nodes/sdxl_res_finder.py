class SDXLResFinder:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
            }
        }

    RETURN_TYPES = ("INT", "INT")
    RETURN_NAMES = ("width", "height")
    FUNCTION = "find_resolution"
    CATEGORY = "MyCustomNodes"

    RESOLUTIONS = [
        (1024, 1024),
        (1152, 896),
        (1216, 832),
        (1344, 768),
        (1536, 640),
    ]

    def find_resolution(self, image):
        _, height, width, _ = image.shape

        if width < height:
            candidates = [(h, w) for w, h in self.RESOLUTIONS]
        else:
            candidates = self.RESOLUTIONS

        image_ratio = width / height
        best_match = min(
            candidates,
            key=lambda res: abs((res[0] / res[1]) - image_ratio)
        )

        return best_match
