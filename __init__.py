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
from .py.nodes.res_finder import ResFinder
from .py.nodes.sdxl_res_finder import SDXLResFinder
from .py.nodes.one_m_scale import OneMScale
from .py.nodes.group_manager import GroupManager
from .py.nodes.character_prompt import CharacterPrompt
from .py.nodes.character_prompt_with_lora import CharacterPromptWithLora
from .py.nodes.character_prompt_with_lora_dual_model import CharacterPromptWithLoraWithDualModel
from .py.nodes.switch import Switch
from .py.nodes.resolution_switch import ResolutionSwitch
from .py.nodes.resolution_selector import ResolutionSelector
from .py.nodes.resolution_finder import ResolutionFinder
from .py.nodes.krea2_lora_util import Krea2LoraUtil
from .py.nodes.json_prompt import JSONPrompt

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
    "ResFinder": ResFinder,
    "SDXLResFinder": SDXLResFinder,
    "OneMScale": OneMScale,
    "GroupManager": GroupManager,
    "CharacterPrompt": CharacterPrompt,
    "CharacterPromptWithLora": CharacterPromptWithLora,
    "CharacterPromptWithLoraWithDualModel": CharacterPromptWithLoraWithDualModel,
    "Switch": Switch,
    "ResolutionSwitch": ResolutionSwitch,
    "ResolutionSelector": ResolutionSelector,
    "ResolutionFinder": ResolutionFinder,
    "Krea2LoraUtil": Krea2LoraUtil,
    "JSONPrompt": JSONPrompt,
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
    "ResFinder": "Resolution Finder (2MP)",
    "SDXLResFinder": "SDXL Resolution Finder",
    "OneMScale": "1m_Scale",
    "GroupManager": "Group Manager",
    "CharacterPrompt": "Character Prompt",
    "CharacterPromptWithLora": "Character Prompt with Lora",
    "CharacterPromptWithLoraWithDualModel": "Character Prompt with Lora Dual Model",
    "Switch": "Switch",
    "ResolutionSwitch": "Resolution Switch",
    "ResolutionSelector": "Resolution Selector",
    "ResolutionFinder": "Resolution Finder",
    "Krea2LoraUtil": "Krea2 Lora Util",
    "JSONPrompt": "JSON Prompt",
}

# Specify the web directory for the gallery's JavaScript
WEB_DIRECTORY = "js"

# Define what is exposed when the module is imported
__all__ = [
    'NODE_CLASS_MAPPINGS',
    'NODE_DISPLAY_NAME_MAPPINGS',
    'WEB_DIRECTORY'
]
