
import torch

class Gallery:
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

    def create_gallery(self, image=None, gallery=None):
        new_gallery = gallery if gallery is not None else []
        if image is not None:
            # The new image is a tensor, add it to the list
            new_gallery.append(image)
        
        # The UI part sends the images to the frontend.
        # We need to prepare a list of image info dicts.
        ui_images = []
        for i, img_tensor in enumerate(new_gallery):
            # We need to give each image a unique filename for the frontend to fetch.
            # ComfyUI's API uses filename, subfolder, and type.
            ui_images.append({
                "filename": f"gallery_img_{i}.png",
                "subfolder": "",
                "type": "temp", # Use temp for preview images
                "tensor": img_tensor # Pass the actual tensor
            })

        # The result is a tuple containing the gallery list for the next node.
        # The "ui" key holds the data for the frontend widget.
        return {"ui": {"images": ui_images}, "result": (new_gallery,)}

# Node class mappings
NODE_CLASS_MAPPINGS = {
    "Gallery": Gallery
}

# Node display name mappings
NODE_DISPLAY_NAME_MAPPINGS = {
    "Gallery": "Gallery Node"
}
