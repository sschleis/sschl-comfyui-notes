
import torch
import folder_paths
from PIL import Image
import numpy as np
import os

class Gallery:
    def __init__(self):
        self.output_dir = folder_paths.get_temp_directory()
        self.type = "temp"

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                 "trigger": (["on", "off"], {"default": "on"}),
            },
            "optional": {
                "image": ("IMAGE",),
                "gallery": ("GALLERY",)
            }
        }

    RETURN_TYPES = ("GALLERY",)
    FUNCTION = "create_gallery"
    CATEGORY = "Notes"
    OUTPUT_NODE = True

    def create_gallery(self, trigger, image=None, gallery=None):
        if trigger == 'off':
            # If triggered off, we can return the existing gallery without changes
            # or an empty one if none exists.
            return (gallery if gallery is not None else [],)

        new_gallery = gallery if gallery is not None else []
        if image is not None:
            new_gallery.append(image)

        ui_images = []
        for i, tensor_image in enumerate(new_gallery):
            # Convert tensor to PIL Image
            img_np = tensor_image.squeeze(0).cpu().numpy()
            img_pil = Image.fromarray((img_np * 255).astype(np.uint8))
            
            # Save the image to a temporary file
            filename = f"gallery_{i}_{np.random.randint(100000)}.png"
            file_path = os.path.join(self.output_dir, filename)
            img_pil.save(file_path)
            
            # Add image info for the frontend
            ui_images.append({
                "filename": filename,
                "subfolder": "",
                "type": self.type
            })

        return {"ui": {"images": ui_images}, "result": (new_gallery,)}

NODE_CLASS_MAPPINGS = {
    "Gallery": Gallery
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Gallery": "Gallery Node"
}
