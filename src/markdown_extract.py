import re

from src.htmlnode import HTMLNode
from src.textnode import TextNode, TextType

IMAGES_RE = r"!\[(.*?)\]\((.*?)\)"
LINK_RE = r"\[(.*?)\]\((.*?)\)"
BOLD_RE = r"\*\*(.*?)\*\*"
ITALIC_RE = r"\*(.*?)\*"
CODE_RE = r"`(.*?)`"


def extract_markdown_elements(text: str, regex_pattern: str):
    if not text:
        return []
    finds = re.findall(regex_pattern, text)
    return finds


def extract_title(markdown: str) -> str:
    markdown_blocks = markdown_to_blocks(markdown)

    for block in markdown_blocks:
        block_type = block_to_block_type(block)

        if block_type == "header":
            html_node = header_to_html(block)

        return html_node.value


def split_nodes_bold_italic_code(nodes: list[TextNode]) -> list[TextNode]:
    index = 0
    while index < len(nodes):
        finds_bold, finds_code, finds_italic, finds, to_update = [], [], [], [], []
        if nodes[index].text_type is not TextType.TEXT:
            index += 1
            continue

        if nodes[index].text == "":
            return nodes

        finds_bold = extract_markdown_elements(nodes[index].text, BOLD_RE)
        finds_italic = extract_markdown_elements(nodes[index].text, ITALIC_RE)
        finds_code = extract_markdown_elements(nodes[index].text, CODE_RE)
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
            to_update.append(TextNode(sections[0], TextType.TEXT))

        if len(nodes[index].text) > 1:
            to_update.append(TextNode(finds[0], text_type))

        if sections[1] != "":
            original_text = sections[1]
            to_update.append(TextNode(original_text, TextType.TEXT))

        nodes[index : index + 1] = to_update

    return nodes


def split_nodes_image_link(nodes: list[TextNode]):
    index = 0
    while index < len(nodes):
        finds_image, finds_links, finds, to_update = [], [], [], []
        if nodes[index].text_type is not TextType.TEXT:
            index += 1
            continue

        if nodes[index].text == "":
            return nodes

        finds_image = extract_markdown_elements(nodes[index].text, IMAGES_RE)
        finds_links = extract_markdown_elements(nodes[index].text, LINK_RE)

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
            to_update.append(TextNode(sections[0], TextType.TEXT))

        if len(nodes[index].text) > 1:
            to_update.append(TextNode(finds[0][0], text_type, finds[0][1]))

        if sections[1] != "":
            original_text = sections[1]
            to_update.append(TextNode(original_text, TextType.TEXT))

        nodes[index : index + 1] = to_update

    return nodes


def markdown_to_blocks(markdown: str):
    markdown_list = markdown.split("\n\n")
    final_list = []
    for item in markdown_list:
        if item == "":
            continue
        final_list.append(item.strip())
    return final_list


def block_to_block_type(block: str):
    if block.startswith("#"):
        return "header"
    if block.startswith("```") and block.endswith("```"):
        return "code"
    if block.startswith(">"):
        return "quote"
    if block.startswith("*") or block.startswith("-"):
        return "unordered_list"
    if int(block.split(".")[0]):
        return "ordered_list"


def markdown_to_html_node(markdown: str):
    markdown_blocks = markdown_to_blocks(markdown)
    html_list = []
    for block in markdown_blocks:
        block_type = block_to_block_type(block)

        if block_type == "header":
            html_node = header_to_html(block)
        elif block_type == "code":
            html_node = code_to_html(block)
        elif block_type == "quote":
            html_node = quote_to_html(block)
        elif block_type == "unordered_list":
            html_node = unordered_list_to_html(block)
        elif block_type == "ordered_list":
            html_node = ordered_list_to_html(block)
        else:
            html_node = HTMLNode(tag="p", value=block)

        if html_node:
            html_list.append(html_node)
    return html_list


def header_to_html(block: str) -> HTMLNode:
    header_size = len(
        list(filter(lambda x: x == "#", block))
    )  # Calculate the number of # in a quote
    text = block.split(header_size * "#")[
        1
    ].strip()  # Split after nth #`s so we have the quoted text
    return HTMLNode(f"h{header_size}", value=text)


def code_to_html(block: str):
    text = block.split("```")[1].strip()
    return HTMLNode("code", value=text)


def quote_to_html(block: str):
    text = block.split(">")[1].strip()
    return HTMLNode("blockquote", value=text)


def unordered_list_to_html(block: str):
    list_items = block.split("\n")
    children_list = []
    for item in list_items:
        text = item.split("-")[1].strip()
        children_list.append(HTMLNode("ol", text))

    return HTMLNode("ul", children=children_list)


def ordered_list_to_html(block: str):
    list_items = block.split("\n")
    children_list = []
    for index, item in enumerate(list_items):
        text = item.split(f"{index+1}.")[1].strip()
        children_list.append(HTMLNode("li", text))

    return HTMLNode("ol", children=children_list)


def text_to_textnodes(text: str):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_bold_italic_code(nodes)
    nodes = split_nodes_image_link(nodes)
    return nodes
