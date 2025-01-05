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


def split_nodes_image(old_nodes):
    new_nodes_list: list[TextNode] = []
    for node in old_nodes:
        if node.text == "":
            # Condition to leave recursion, at the last split, the text will be an empty string
            return new_nodes_list

        link_finds = extract_markdown_images(node.text)
        text_to_split = f"[{link_finds[0][0]}]({link_finds[0][1]})"
        node_split = node.text.split(text_to_split)

        new_nodes_list.extend([TextNode(f"{node_split[0]}", TextType.TEXT)])
        new_nodes_list.extend([TextNode(f"{text_to_split}", TextType.IMAGE)])
        # Call the function recursively, with the text from the second split.
        # This is called as many links as there are in the text.
        new_nodes_list.extend(
            split_nodes_link(
                [TextNode(node_split[1], TextType.TEXT)],
            )
        )
    return new_nodes_list


def split_nodes_link(old_nodes: list[TextNode]):
    new_nodes_list: list[TextNode] = []
    for node in old_nodes:
        if node.text == "":
            # Condition to leave recursion, at the last split, the text will be an empty string
            return new_nodes_list

        link_finds = extract_markdown_links(node.text)
        text_to_split = f"[{link_finds[0][0]}]({link_finds[0][1]})"
        node_split = node.text.split(text_to_split)

        new_nodes_list.extend([TextNode(f"{node_split[0]}", TextType.TEXT)])
        new_nodes_list.extend([TextNode(f"{text_to_split}", TextType.LINK)])
        # Call the function recursively, with the text from the second split.
        # This is called as many links as there are in the text.
        new_nodes_list.extend(
            split_nodes_link(
                [TextNode(node_split[1], TextType.TEXT)],
            )
        )

    return new_nodes_list


def extract_markdown_images(text: str):
    finds = re.findall(IMAGES_RE, text)
    return finds


def extract_markdown_links(text: str):
    finds = re.findall(LINK_RE, text)
    return finds
