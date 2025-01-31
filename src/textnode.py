from enum import Enum
from src.htmlnode import LeafNode
from utils import move_files_to_another_directory
from pathlib import Path

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "links"
    IMAGE = "image"


class TextNode:
    def __init__(self, text: str, text_type: TextType, url: str | None = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other: "TextNode"):  # type: ignore
        if (
            other.text == self.text
            and other.text_type == self.text_type
            and other.url == self.url
        ):
            return True

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"


def text_node_to_html_node(text_node: TextNode):
    if text_node.text_type not in TextType:
        raise ValueError(f"Text Type should be one of {TextType}")

    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, value=text_node.text)
    if text_node.text_type == TextType.BOLD:
        return LeafNode(tag="b", value=text_node.text)
    if text_node.text_type == TextType.ITALIC:
        return LeafNode(tag="i", value=text_node.text)
    if text_node.text_type == TextType.CODE:
        return LeafNode(tag="code", value=text_node.text)
    if text_node.text_type == TextType.LINK:
        return LeafNode(tag="a", value=text_node.text, props={"href": text_node.url})
    if text_node.text_type == TextType.IMAGE:
        return LeafNode(
            tag="img", value="", props={"src": text_node.url, "alt": text_node.text}
        )


def main():
    object_1 = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
    move_files_to_another_directory(Path("static"), Path("public"))
    print(object_1.__repr__())


if __name__ == "__main__":
    main()
