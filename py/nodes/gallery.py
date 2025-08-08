import torch
import folder_paths
from PIL import Image
import numpy as np
import os
import server

class Gallery:
    def __init__(self):
        self.output_dir = folder_paths.get_temp_directory()
        self.type = "temp"
        self.server = server.PromptServer.instance

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {},
            "optional": {
                "image": ("IMAGE",),
                "gallery": ("GALLERY",)
            },
            "hidden": {"prompt": "PROMPT", "extra_pnginfo": "EXTRA_PNGINFO"}, # Add hidden inputs
        }

    RETURN_TYPES = ("GALLERY",)
    FUNCTION = "create_gallery"
    CATEGORY = "Notes"
    OUTPUT_NODE = True 

    def create_gallery(self, prompt, extra_pnginfo, gallery=None, **kwargs):
        new_gallery = gallery if isinstance(gallery, list) else []
        
        # Find the node_id for this node in the prompt
        node_id = None
        for i in prompt:
            if prompt[i]["class_type"] == "Gallery":
                node_id = i
                break

        # Clear the existing gallery on new execution
        if node_id:
            self.server.send_sync("sschl-gallery-clear", {"node_id": node_id})

        # Process all incoming images and send them one by one
        for key, value in kwargs.items():
            if value is not None and isinstance(value, torch.Tensor):
                images = list(value) if value.dim() == 4 else [value]
                for tensor_image in images:
                    new_gallery.append(tensor_image)
                    
                    img_np = tensor_image.squeeze(0).cpu().numpy()
                    img_pil = Image.fromarray((img_np * 255).astype(np.uint8))
                    
                    filename = f"gallery_temp_{len(new_gallery)}_{np.random.randint(100000)}.png"
                    file_path = os.path.join(self.output_dir, filename)
                    img_pil.save(file_path)
                    
                    if node_id:
                        image_data = {
                            "filename": filename,
                            "subfolder": "",
                            "type": self.type
                        }
                        self.server.send_sync("sschl-gallery-update", {"node_id": node_id, "image": image_data})

        return (new_gallery,)

NODE_CLASS_MAPPINGS = {
    "Gallery": Gallery
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Gallery": "Gallery Node"
}