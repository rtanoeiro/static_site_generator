import re

IMAGES_RE = r"!\[(.*?)\]\((.*?)\)"
LINK_RE = r"\[(.*?)\]\((.*?)\)"


def extract_markdown_images(text: str):
    finds = re.findall(IMAGES_RE, text)
    return finds


def extract_markdown_links(text: str):
    finds = re.findall(LINK_RE, text)
    return finds
