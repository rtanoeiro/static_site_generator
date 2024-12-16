import unittest

from htmlnode import HTMLNode


class TestHTMLtNode(unittest.TestCase):
    def test_props_empty(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")

    def test_props_data(self):
        node = HTMLNode(props={"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(
            node.props_to_html(), ' href="https://www.google.com" target="_blank"'
        )

    def test_html_values(self):
        node = HTMLNode(tag="a", value="This is some text", children=None, props=None)
        self.assertEqual(node.tag, "a")
        self.assertEqual(node.value, "This is some text")
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)
