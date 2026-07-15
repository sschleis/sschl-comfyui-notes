class ResolutionFinder:
    MEGAPIXELS = {
        "1MP": 1_000_000,
        "2MP": 2_000_000,
        "4MP": 4_000_000,
    }

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "megapixels": (list(cls.MEGAPIXELS.keys()), {"default": "2MP"}),
            }
        }

    RETURN_TYPES = ("INT", "INT")
    RETURN_NAMES = ("width", "height")
    FUNCTION = "find_resolution"
    CATEGORY = "MyCustomNodes"

    def find_resolution(self, image, megapixels):
        # ComfyUI Bilder haben das Format [B, H, W, C]
        _, height, width, _ = image.shape

        target_pixels = self.MEGAPIXELS[megapixels]
        aspect_ratio = width / height

        # w * h = target_pixels, w = h * ratio -> h = sqrt(target_pixels / ratio)
        new_h = (target_pixels / aspect_ratio) ** 0.5
        new_w = new_h * aspect_ratio

        # Auf Vielfache von 8 runden (Standard für Diffusionsmodelle)
        new_w = max(8, round(new_w / 8) * 8)
        new_h = max(8, round(new_h / 8) * 8)

        return (int(new_w), int(new_h))
