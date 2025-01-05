from enum import Enum
from htmlnode import LeafNode


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
        return LeafNode(tag="a", value=text_node.text)
    if text_node.text_type == TextType.IMAGE:
        return LeafNode(
            tag="img", value="", props={"src": text_node.url, "alt": text_node.text}
        )


def split_nodes_delimiter(old_nodes: list[TextNode], delimiter, text_type):
    new_nodes_list = []

    for node in old_nodes:
        node_split = node.text.split(delimiter)
        for index, item in enumerate(node_split):
            # Only the middle element contains the new text type:
            if index % 2 == 0:
                new_nodes_list.append(TextNode(f"{item}", TextType.TEXT))
            else:
                new_nodes_list.append(TextNode(f"{item}", text_type))

    return new_nodes_list


def main():
    object_1 = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
    print(object_1.__repr__())


if __name__ == "__main__":
    main()
