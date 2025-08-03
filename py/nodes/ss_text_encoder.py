class SSchlTextEncoder:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "clip": ("CLIP",),
                "text": ("STRING", {"forceInput": True}),
            }
        }

    RETURN_TYPES = ("CONDITIONING",)
    FUNCTION = "encode"
    CATEGORY = "MyCustomNodes"

    def encode(self, clip, text):
        # Ensure text is a single string, as it might come as a list/tuple
        if isinstance(text, (list, tuple)):
            text_to_encode = "\n".join(text)
        else:
            text_to_encode = str(text)

        # Use the clip object's methods for encoding, similar to standard CLIPTextEncode
        tokens = clip.tokenize(text_to_encode)
        
        # Check if the CLIP model supports pooled output
        if hasattr(clip, 'is_pooled') and clip.is_pooled:
            cond, pooled = clip.encode_from_tokens(tokens, return_pooled=True)
        else:
            cond = clip.encode_from_tokens(tokens, return_pooled=False)
            pooled = None

        return ([[cond, {"pooled_output": pooled}]],)