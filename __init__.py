import os
import importlib.util
import sys

# Add the parent directory of 'py' to the system path
# This is necessary for the imports to work correctly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}

# Set the web directory for JavaScript files
WEB_DIRECTORY = "js"

def load_nodes():
    """
    Dynamically loads all node modules from the 'py/nodes' directory.
    """
    nodes_dir = os.path.join(os.path.dirname(__file__), "py", "nodes")
    if not os.path.isdir(nodes_dir):
        return

    for filename in os.listdir(nodes_dir):
        if filename.endswith(".py") and not filename.startswith("__"):
            module_name = filename[:-3]
            module_path = os.path.join(nodes_dir, filename)
            
            try:
                spec = importlib.util.spec_from_file_location(f"sschl_comfyui_notes.py.nodes.{module_name}", module_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                if hasattr(module, "NODE_CLASS_MAPPINGS"):
                    NODE_CLASS_MAPPINGS.update(module.NODE_CLASS_MAPPINGS)
                
                if hasattr(module, "NODE_DISPLAY_NAME_MAPPINGS"):
                    NODE_DISPLAY_NAME_MAPPINGS.update(module.NODE_DISPLAY_NAME_MAPPINGS)
            except Exception as e:
                print(f"[ERROR] Failed to load node from {filename}: {e}")

load_nodes()

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS', 'WEB_DIRECTORY']