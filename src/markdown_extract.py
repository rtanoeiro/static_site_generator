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


def split_nodes_bold_italic_code(nodes: list[TextNode]) -> list[TextNode]:
    index = 0
    while index < len(nodes):
        finds_bold, finds_code, finds_italic, finds = [], [], [], []
        nodes_to_update = []
        if nodes[index].text_type is not TextType.TEXT:
            index += 1
            continue

        if nodes[index].text == "":
            return nodes

        finds_bold = extract_markdown_bold(nodes[index].text)
        finds_italic = extract_markdown_italic(nodes[index].text)
        finds_code = extract_markdown_code(nodes[index].text)
        if finds_code:
            delimiter = "`"
            finds = finds_code
            text_type = TextType.CODE
        elif finds_bold:
            delimiter = "**"
            finds = finds_bold
            text_type = TextType.BOLD
        elif finds_italic:
            delimiter = "*"
            finds = finds_italic
            text_type = TextType.ITALIC

        if not finds:
            index += 1
            continue

        sections = nodes[index].text.split(f"{delimiter}{finds[0]}{delimiter}", 1)

        if len(sections) != 2:
            raise ValueError("Invalid markdown, image section not closed")

        if sections[0] != "":
            nodes_to_update.append(TextNode(sections[0], TextType.TEXT))

        if len(nodes[index].text) > 1:
            nodes_to_update.append(TextNode(finds[0], text_type))

        if sections[1] != "":
            original_text = sections[1]
            nodes_to_update.append(TextNode(original_text, TextType.TEXT))

        nodes[index : index + 1] = nodes_to_update

    return nodes


def split_nodes_image_link(nodes: list[TextNode]):
    index = 0
    while index < len(nodes):
        finds_image, finds_links, finds, nodes_to_update = [], [], [], []
        if nodes[index].text_type is not TextType.TEXT:
            index += 1
            continue

        if nodes[index].text == "":
            return nodes

        finds_image = extract_markdown_images(nodes[index].text)
        finds_links = extract_markdown_links(nodes[index].text)

        if finds_image:
            finds = finds_image
            text_type = TextType.IMAGE
        elif finds_links:
            finds = finds_links
            text_type = TextType.LINK

        if not finds:
            index += 1
            continue

        if text_type == TextType.IMAGE:
            sections = nodes[index].text.split(f"![{finds[0][0]}]({finds[0][1]})", 1)
        if text_type == TextType.LINK:
            sections = nodes[index].text.split(f"[{finds[0][0]}]({finds[0][1]})", 1)

        if len(sections) != 2:
            raise ValueError("Invalid markdown, image section not closed")
        if sections[0] != "":
            nodes_to_update.append(TextNode(sections[0], TextType.TEXT))

        if len(nodes[index].text) > 1:
            nodes_to_update.append(TextNode(finds[0][0], text_type, finds[0][1]))

        if sections[1] != "":
            original_text = sections[1]
            nodes_to_update.append(TextNode(original_text, TextType.TEXT))

        nodes[index : index + 1] = nodes_to_update

    return nodes


def text_to_textnodes(text: str):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_bold_italic_code(nodes)
    nodes = split_nodes_image_link(nodes)
    return nodes
