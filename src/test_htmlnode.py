import unittest

from htmlnode import HTMLNode, LeafNode


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

    def test_leaf_raise_error(self):
        node = LeafNode(tag="a", value=None, props={"href": "https://www.google.com"})
        with self.assertRaises(ValueError):
            node.to_html()

    def test_leaf_node_build(self):
        node = LeafNode(
            tag="a", value="Google Website", props={"href": "https://www.google.com"}
        )
        self.assertEqual(
            node.to_html(), '<a href="https://www.google.com">Google Website</a>'
        )

    def test_to_html_no_children(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")
