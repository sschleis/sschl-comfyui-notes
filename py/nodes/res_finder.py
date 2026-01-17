import torch

class ResFinder:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
            }
        }

    RETURN_TYPES = ("INT", "INT")
    RETURN_NAMES = ("width", "height")
    FUNCTION = "calculate_res"
    CATEGORY = "MyCustomNodes"

    def calculate_res(self, image):
        # ComfyUI Bilder haben das Format [B, H, W, C]
        # Wir nehmen das erste Bild aus dem Batch
        _, height, width, _ = image.shape
        
        target_pixels = 2_000_000
        aspect_ratio = width / height
        
        # Berechnung:
        # w * h = 2,000,000
        # (h * ratio) * h = 2,000,000
        # h^2 * ratio = 2,000,000
        # h = sqrt(2,000,000 / ratio)
        
        new_h = (target_pixels / aspect_ratio) ** 0.5
        new_w = new_h * aspect_ratio
        
        # In Integer konvertieren
        return (int(round(new_w)), int(round(new_h)))
