import torch
import torch.nn.functional as F

class OneMScale:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "scale_image"
    CATEGORY = "MyCustomNodes"

    def scale_image(self, image):
        # ComfyUI Bilder haben das Format [Batch, Height, Width, Channels]
        # Wir arbeiten hier mit dem gesamten Batch
        batch, height, width, channels = image.shape
        
        num_pixels = width * height
        target_pixels = 1_000_000 # 1 Megapixel

        if num_pixels <= target_pixels:
            # Bild hat 1MP oder weniger -> einfach zurückgeben
            return (image,)

        # Berechnung der neuen Dimensionen unter Beibehaltung des Seitenverhältnisses
        aspect_ratio = width / height
        
        # w * h = target_pixels
        # (h * aspect_ratio) * h = target_pixels
        # h^2 = target_pixels / aspect_ratio
        new_h = int((target_pixels / aspect_ratio) ** 0.5)
        new_w = int(new_h * aspect_ratio)

        # PyTorch Interpolate erwartet [Batch, Channels, Height, Width]
        # Also permutieren wir von [B, H, W, C] zu [B, C, H, W]
        img = image.permute(0, 3, 1, 2)
        
        # Skalierung durchführen
        img = F.interpolate(img, size=(new_h, new_w), mode='bilinear', align_corners=False)
        
        # Zurück permutieren zu [B, H, W, C]
        img = img.permute(0, 2, 3, 1)

        return (img,)
