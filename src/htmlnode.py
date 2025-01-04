class HTMLNode:
    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        children=None,
        props: dict[str, str] | None = None,
    ):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if self.props is None:
            return ""
        props_html = ""
        for prop in self.props:
            props_html += f' {prop}="{self.props[prop]}"'
        return props_html


class LeafNode(HTMLNode):
    def __init__(self, tag, value, children=None, props=None):
        super().__init__(tag, value, children, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("Leaf nodes must have a value")
        if self.tag is None:
            return self.value

        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    def __init__(self, tag, children: list[HTMLNode], value=None, props=None):
        super().__init__(tag, value, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("Parent nodes must have a tag")

        if self.children is None:
            raise ValueError("Parent nodes must have a children")

        html_text = ""
        for child in self.children:
            if isinstance(child, list):
                html_text += child.to_html()
            html_text += child.to_html()
        return f"<{self.tag}>{html_text}</{self.tag}>"
