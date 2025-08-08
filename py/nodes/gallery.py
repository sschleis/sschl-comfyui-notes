
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
        # Although we handle dynamic inputs, we define the initial ones for clarity.
        # The JS part will add more inputs named image_1, image_2, etc.
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
        # Initialize the gallery. If an existing gallery is passed, use it.
        new_gallery = gallery if gallery is not None else []

        # Process all incoming keyword arguments.
        # This will include 'image', 'image_1', 'image_2', etc.
        for key, value in kwargs.items():
            # We are only interested in image tensors.
            if value is not None and isinstance(value, torch.Tensor):
                # ComfyUI can pass images as a single tensor or a batch of tensors.
                # We handle both cases by checking the dimensions.
                if value.dim() == 4: # Batch of images
                    new_gallery.extend(list(value))
                elif value.dim() == 3: # Single image
                    new_gallery.append(value)

        ui_images = []
        for i, tensor_image in enumerate(new_gallery):
            if not isinstance(tensor_image, torch.Tensor):
                continue # Skip any non-tensor data that might have slipped in.

            # Convert tensor to a PIL Image for saving.
            # Tensors are expected to be in CHW format, so we might need to adjust if not.
            img_np = tensor_image.squeeze(0).cpu().numpy()
            img_pil = Image.fromarray((img_np * 255).astype(np.uint8))
            
            # Save the image to a temporary file that the frontend can access.
            filename = f"gallery_temp_{i}_{np.random.randint(100000)}.png"
            file_path = os.path.join(self.output_dir, filename)
            img_pil.save(file_path)
            
            # Provide the necessary info for the frontend to display the image.
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
