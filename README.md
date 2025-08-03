# sschl-comfyui-notes

Meine ersten Custom Nodes für ComfyUI.

## Installation

1.  Clone this repository into your `ComfyUI/custom_nodes/` directory:
    ```bash
    cd ComfyUI/custom_nodes/
    git clone https://github.com/sschleis/sschl-comfyui-notes.git
    ```
2.  Restart ComfyUI.

## File Structure

The project is structured as follows:

-   `__init__.py`: The main entry point that registers the custom nodes with ComfyUI.
-   `py/nodes/`: This directory contains the individual Python files for each node.
    -   `add_numbers.py`: The "Add Numbers" node.
    -   `float_to_str.py`: The "Float to String" node.
    -   `input_text.py`: The "Input Text" node.
    -   `show_text.py`: The "Show Text" node.

## Verfügbare Nodes

*   **Add Numbers**: Ein einfacher Node, der zwei Zahlen addiert.
*   **Float to String**: Wandelt einen Float-Wert in einen String um.
*   **Show Text**: Zeigt einen Text an.
*   **Input Text**: Ermöglicht die Eingabe von Text, der an andere Nodes weitergegeben werden kann.
