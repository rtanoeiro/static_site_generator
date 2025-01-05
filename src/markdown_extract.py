import re
from textnode import TextNode, TextType

IMAGES_RE = r"!\[(.*?)\]\((.*?)\)"
LINK_RE = r"\[(.*?)\]\((.*?)\)"


def split_nodes_delimiter(old_nodes: list[TextNode], delimiter, text_type):
    new_nodes_list = []

    for node in old_nodes:
        node_split = node.text.split(delimiter)
        for index, item in enumerate(node_split):
            if item == "":
                continue
            if index % 2 == 0:
                new_nodes_list.append(TextNode(f"{item}", TextType.TEXT))
            else:
                new_nodes_list.append(TextNode(f"{item}", text_type))

    return new_nodes_list


def extract_markdown_images(text: str):
    finds = re.findall(IMAGES_RE, text)
    return finds


def extract_markdown_links(text: str):
    finds = re.findall(LINK_RE, text)
    return finds
