from enum import Enum


class TextType(Enum):
    NORMAL = "normal"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "links"
    IMAGES = "images"


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


def main():
    object_1 = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
    print(object_1.__repr__())


if __name__ == "__main__":
    main()
