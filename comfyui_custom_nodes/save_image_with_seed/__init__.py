from nodes import SaveImage


class SaveImageWithSeed(SaveImage):
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE", {"tooltip": "The images to save."}),
                "filename_prefix": (
                    "STRING",
                    {
                        "default": "asatake_yoshino_manual",
                        "tooltip": "The base filename prefix. The first KSampler seed is appended automatically.",
                    },
                ),
            },
            "hidden": {
                "prompt": "PROMPT",
                "extra_pnginfo": "EXTRA_PNGINFO",
            },
        }

    RETURN_TYPES = ()
    FUNCTION = "save_images_with_seed"
    OUTPUT_NODE = True
    CATEGORY = "image"
    DESCRIPTION = "Saves images with the current KSampler seed appended to the filename."

    @staticmethod
    def _find_ksampler_seed(prompt):
        if not isinstance(prompt, dict):
            return None

        for node in prompt.values():
            if not isinstance(node, dict):
                continue
            if node.get("class_type") not in {"KSampler", "KSamplerAdvanced"}:
                continue
            inputs = node.get("inputs", {})
            seed = inputs.get("seed")
            if isinstance(seed, (int, str)):
                return str(seed)

        return None

    def save_images_with_seed(self, images, filename_prefix="asatake_yoshino_manual", prompt=None, extra_pnginfo=None):
        seed = self._find_ksampler_seed(prompt)
        if seed:
            filename_prefix = f"{filename_prefix}_seed{seed}"
        return super().save_images(images, filename_prefix, prompt, extra_pnginfo)


NODE_CLASS_MAPPINGS = {
    "SaveImageWithSeed": SaveImageWithSeed,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "SaveImageWithSeed": "Save Image With Seed",
}
