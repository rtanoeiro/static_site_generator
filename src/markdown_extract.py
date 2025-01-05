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


def split_nodes_image(old_nodes: list[TextNode]):
    new_nodes_list: list[TextNode] = []
    for node in old_nodes:
        # In case the text node is not IMAGE type
        if node.text_type != TextType.TEXT:
            new_nodes_list.append(node)
            continue

        if node.text == "":
            # Condition to leave recursion, at the last split, the text will be an empty string
            return new_nodes_list

        link_finds = extract_markdown_images(node.text)
        image_text, image_url = link_finds[0][0], link_finds[0][1]

        text_to_split = f"![{image_text}]({image_url})"
        node_split = node.text.split(text_to_split)

        if node_split[0] != "":
            new_nodes_list.extend([TextNode(f"{node_split[0]}", TextType.TEXT)])

        new_nodes_list.extend([TextNode(image_text, TextType.IMAGE, url=image_url)])
        # Call the function recursively, with the text from the second split.
        # This is called as many links as there are in the text.
        new_nodes_list.extend(
            split_nodes_image(
                [TextNode(node_split[1], TextType.TEXT)],
            )
        )
    return new_nodes_list


def split_nodes_link(old_nodes: list[TextNode]):
    new_nodes_list: list[TextNode] = []
    for node in old_nodes:
        # In case the text node is not IMAGE type
        if node.text_type != TextType.TEXT:
            new_nodes_list.append(node)
            continue

        if node.text == "":
            # Condition to leave recursion, at the last split, the text will be an empty string
            return new_nodes_list

        link_finds = extract_markdown_links(node.text)
        link_text, link_url = link_finds[0][0], link_finds[0][1]
        text_to_split = f"[{link_text}]({link_url})"
        node_split = node.text.split(text_to_split)

        if node_split[0] != "":
            new_nodes_list.extend([TextNode(f"{node_split[0]}", TextType.TEXT)])

        new_nodes_list.extend([TextNode(link_text, TextType.LINK, link_url)])
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


node = TextNode(
    "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
    TextType.TEXT,
)
new_nodes = split_nodes_image([node])
print(new_nodes)
