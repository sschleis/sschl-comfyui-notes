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
            "required": {},
            "optional": {
                "image": ("IMAGE",),
                "gallery": ("GALLERY",)
            }
        }

    RETURN_TYPES = ("GALLERY",)
    FUNCTION = "create_gallery"
    CATEGORY = "Notes"
    OUTPUT_NODE = True

    def create_gallery(self, gallery=None, **kwargs):
        new_gallery = gallery if gallery is not None else []

        # Collect all image inputs, including dynamic ones like image, image_1, image_2 etc.
        for key, value in kwargs.items():
            if key.startswith('image') and value is not None:
                # In ComfyUI, images can be single tensors or a batch (list of tensors)
                if isinstance(value, list):
                    new_gallery.extend(value)
                else:
                    new_gallery.append(value)

        ui_images = []
        for i, tensor_image in enumerate(new_gallery):
            if not isinstance(tensor_image, torch.Tensor):
                continue # Skip non-tensor items that might be in the list

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