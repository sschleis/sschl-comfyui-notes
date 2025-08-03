from .py.nodes.add_numbers import AddNumbers
from .py.nodes.float_to_str import FloatToStr
from .py.nodes.input_text import InputText
from .py.nodes.show_text import ShowText
from .py.nodes.combine_strings import CombineStrings
from .py.nodes.text_appender import TextAppender

NODE_CLASS_MAPPINGS = {
    "AddNumbers": AddNumbers,
    "FloatToStr": FloatToStr,
    "InputText": InputText,
    "ShowText": ShowText,
    "CombineStrings": CombineStrings,
    "TextAppender": TextAppender,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "AddNumbers": "Add Numbers",
    "FloatToStr": "Float to String",
    "InputText": "Input Text",
    "ShowText": "Show Text",
    "CombineStrings": "Combine Strings",
    "TextAppender": "Text Appender",
}
