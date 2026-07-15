class ResolutionSelector:
    MEGAPIXELS = {
        "1MP": 1_000_000,
        "2MP": 2_000_000,
        "4MP": 4_000_000,
    }

    RATIOS = {
        "1:1 (Quadratisch)": (1, 1),
        "4:3 (Landscape)": (4, 3),
        "3:2 (Landscape)": (3, 2),
        "16:9 (Landscape)": (16, 9),
        "16:10 (Landscape)": (16, 10),
        "21:9 (Landscape)": (21, 9),
        "5:4 (Landscape)": (5, 4),
        "3:4 (Portrait)": (3, 4),
        "2:3 (Portrait)": (2, 3),
        "9:16 (Portrait)": (9, 16),
        "10:16 (Portrait)": (10, 16),
        "9:21 (Portrait)": (9, 21),
        "4:5 (Portrait)": (4, 5),
    }

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "aspect_ratio": (list(cls.RATIOS.keys()), {"default": "1:1 (Quadratisch)"}),
                "megapixels": (list(cls.MEGAPIXELS.keys()), {"default": "2MP"}),
            }
        }

    RETURN_TYPES = ("INT", "INT")
    RETURN_NAMES = ("width", "height")
    FUNCTION = "select_resolution"
    CATEGORY = "MyCustomNodes"

    def select_resolution(self, aspect_ratio, megapixels):
        ratio_w, ratio_h = self.RATIOS[aspect_ratio]
        ratio = ratio_w / ratio_h
        target_pixels = self.MEGAPIXELS[megapixels]

        # w * h = target_pixels, w = h * ratio -> h = sqrt(target_pixels / ratio)
        height = (target_pixels / ratio) ** 0.5
        width = height * ratio

        # Auf Vielfache von 8 runden (Standard für Diffusionsmodelle)
        width = max(8, round(width / 8) * 8)
        height = max(8, round(height / 8) * 8)

        return (int(width), int(height))
