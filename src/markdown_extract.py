import re

from src.htmlnode import ParentNode
from src.textnode import TextNode, TextType, text_node_to_html_node

IMAGES_RE = r"!\[(.*?)\]\((.*?)\)"
LINK_RE = r"\[(.*?)\]\((.*?)\)"
BOLD_RE = r"\*\*(.*?)\*\*"
ITALIC_RE = r"_(.*?)_"
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
            title = block[2:]

        return title


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
            delimiter = "_"
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
    block_lines = block.split("\n")

    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return "header"

    if block.startswith("```") and block.endswith("```"):
        return "code"

    if block.startswith(">"):
        for line in block_lines:
            if not line.startswith(">"):
                return "paragraph"
        return "quote"

    if block.startswith("* ") or block.startswith("- "):
        for line in block_lines:
            if not (block.startswith("* ") or block.startswith("- ")):
                return "paragraph"
        return "unordered_list"

    if block.startswith("1. "):
        i = 1
        for line in block_lines:
            if not line.startswith(f"{i}. "):
                return "paragraph"
            i += 1
        return "ordered_list"
    return "paragraph"


def markdown_to_html_node(markdown: str) -> list[ParentNode]:
    markdown_blocks = markdown_to_blocks(markdown)
    children = []
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
        elif block_type == "paragraph":
            html_node = paragraph_to_html_node(block)

        if html_node:
            children.append(html_node)
    return ParentNode("div", children, None)


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children


def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)


def header_to_html(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"invalid heading level: {level}")
    text = block[level + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)


def code_to_html(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("invalid code block")
    text = block[3:-3]
    children = text_to_children(text)
    code = ParentNode("code", children)
    return ParentNode("pre", [code])


def ordered_list_to_html(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[3:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)


def unordered_list_to_html(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)


def quote_to_html(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)


def text_to_textnodes(text: str):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_bold_italic_code(nodes)
    nodes = split_nodes_image_link(nodes)
    return nodes
