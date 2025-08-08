# Description: Imports all nodes for the sschl-comfyui-notes extension.

# Import all node classes
from .py.nodes.add_numbers import AddNumbers
from .py.nodes.float_to_str import FloatToStr
from .py.nodes.input_text import InputText
from .py.nodes.show_text import ShowText
from .py.nodes.combine_strings import CombineStrings
from .py.nodes.text_appender import TextAppender
from .py.nodes.ss_text_encoder import SSchlTextEncoder
from .py.nodes.character import Character
from .py.nodes.connector import Connector
from .py.nodes.gallery import Gallery

# Add all node classes to the mapping
NODE_CLASS_MAPPINGS = {
    "AddNumbers": AddNumbers,
    "FloatToStr": FloatToStr,
    "InputText": InputText,
    "ShowText": ShowText,
    "CombineStrings": CombineStrings,
    "TextAppender": TextAppender,
    "SSchlTextEncoder": SSchlTextEncoder,
    "Character": Character,
    "Connector": Connector,
    "Gallery": Gallery,
}

# Add all node display names to the mapping
NODE_DISPLAY_NAME_MAPPINGS = {
    "AddNumbers": "Add Numbers",
    "FloatToStr": "Float to String",
    "InputText": "Input Text",
    "ShowText": "Show Text",
    "CombineStrings": "Combine Strings",
    "TextAppender": "Text Appender",
    "SSchlTextEncoder": "SSchl Text Encoder",
    "Character": "Character",
    "Connector": "Connector",
    "Gallery": "Gallery Node",
}

# Specify the web directory for the gallery's JavaScript
WEB_DIRECTORY = "js"

# Define what is exposed when the module is imported
__all__ = [
    'NODE_CLASS_MAPPINGS',
    'NODE_DISPLAY_NAME_MAPPINGS',
    'WEB_DIRECTORY'
]