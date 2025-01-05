import re
from textnode import TextNode, TextType

IMAGES_RE = r"!\[(.*?)\]\((.*?)\)"
LINK_RE = r"\[(.*?)\]\((.*?)\)"
BOLD_RE = r"\*\*(.*?)\*\*"
ITALIC_RE = r"\*(.*?)\*"
CODE_RE = r"`(.*?)`"


def extract_markdown_bold(text: str):
    finds = re.findall(BOLD_RE, text)
    return finds


def extract_markdown_italic(text: str):
    finds = re.findall(ITALIC_RE, text)
    return finds


def extract_markdown_code(text: str):
    finds = re.findall(CODE_RE, text)
    return finds


def extract_markdown_images(text: str):
    finds = re.findall(IMAGES_RE, text)
    return finds


def extract_markdown_links(text: str):
    finds = re.findall(LINK_RE, text)
    return finds


def split_nodes_bold_italic_code(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
):
    new_nodes_list: list[TextNode] = []
    for node in old_nodes:
        # In case the text node is not IMAGE type
        if node.text_type != TextType.TEXT:
            new_nodes_list.append(node)
            continue

        if node.text == "":
            # Condition to leave recursion, at the last split, the text will be an empty string
            return new_nodes_list
        original_text = node.text

        if text_type == TextType.BOLD:
            finds = extract_markdown_bold(original_text)
        if text_type == TextType.ITALIC:
            finds = extract_markdown_italic(original_text)
        if text_type == TextType.CODE:
            finds = extract_markdown_code(original_text)

        if len(finds) == 0:
            continue

        for find in finds:
            sections = original_text.split(f"{delimiter}{find}{delimiter}", 1)

            if len(sections) != 2:
                raise ValueError("Invalid markdown, image section not closed")
            if sections[0] != "":
                new_nodes_list.append(TextNode(sections[0], TextType.TEXT))
            new_nodes_list.append(TextNode(find, text_type))
            # Update the text for the next iteraction
            original_text = sections[1]

    return new_nodes_list, original_text


def split_nodes_image_link(old_nodes: list[TextNode], text_type: TextType):
    new_nodes_list: list[TextNode] = []
    for node in old_nodes:
        # In case the text node is not IMAGE type
        if node.text_type != TextType.TEXT:
            new_nodes_list.append(node)
            continue

        if node.text == "":
            # Condition to leave recursion, at the last split, the text will be an empty string
            return new_nodes_list
        original_text = node.text

        if text_type == TextType.IMAGE:
            finds = extract_markdown_images(original_text)
        if text_type == TextType.LINK:
            finds = extract_markdown_links(original_text)

        if len(finds) == 0:
            continue

        for find in finds:
            if text_type == TextType.IMAGE:
                sections = original_text.split(f"![{find[0]}]({find[1]})", 1)
            if text_type == TextType.LINK:
                sections = original_text.split(f"[{find[0]}]({find[1]})", 1)

            if len(sections) != 2:
                raise ValueError("Invalid markdown, image section not closed")
            if sections[0] != "":
                new_nodes_list.append(TextNode(sections[0], TextType.TEXT))
            new_nodes_list.append(
                TextNode(
                    find[0],
                    text_type,
                    find[1],
                )
            )
            # Update the text for the next iteraction
            original_text = sections[1]

    return new_nodes_list, original_text


# Improve to use a while loop
# Improve to modify the nodes in the function, as text and not text types are automatically skipped!
# This should reduce the need to return original_text
def text_to_textnodes(text: str):
    nodes = [TextNode(text, TextType.TEXT)]
    final_nodes = []
    nodes, new_text = split_nodes_bold_italic_code(nodes, "**", TextType.BOLD)
    final_nodes.extend(nodes)
    nodes, new_text = split_nodes_bold_italic_code(
        [TextNode(new_text, TextType.TEXT)], "*", TextType.ITALIC
    )
    final_nodes.extend(nodes)
    nodes, new_text = split_nodes_bold_italic_code(
        [TextNode(new_text, TextType.TEXT)], "`", TextType.CODE
    )
    final_nodes.extend(nodes)
    nodes, new_text = split_nodes_image_link(
        [TextNode(new_text, TextType.TEXT)], TextType.IMAGE
    )
    final_nodes.extend(nodes)
    nodes, new_text = split_nodes_image_link(
        [TextNode(new_text, TextType.TEXT)], TextType.LINK
    )
    final_nodes.extend(nodes)

    return final_nodes
