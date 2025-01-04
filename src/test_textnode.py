import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_is_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        self.assertEqual(node.text_type, TextType.TEXT)

    def test_is_bold(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node.text_type, TextType.BOLD)

    def test_is_italic(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        self.assertEqual(node.text_type, TextType.ITALIC)

    def test_is_code(self):
        node = TextNode("This is a text node", TextType.CODE)
        self.assertEqual(node.text_type, TextType.CODE)

    def test_is_link(self):
        node = TextNode("This is a text node", TextType.LINK)
        self.assertEqual(node.text_type, TextType.LINK)

    def test_is_image(self):
        node = TextNode("This is a text node", TextType.IMAGE)
        self.assertEqual(node.text_type, TextType.IMAGE)

    def test_none_url(self):
        node = TextNode("This is a text node", TextType.TEXT)
        self.assertEqual(node.url, None)

    def test_is_different(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_text_html_node(self):
        text_node = TextNode("This is a test text node", TextType.TEXT)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.value, "This is a test text node")

    def test_text_html_node_building(self):
        text_node = TextNode("This is a test text node", TextType.TEXT)
        html_node = text_node_to_html_node(text_node).to_html()
        self.assertEqual(html_node, "This is a test text node")

    def test_bold_html_node(self):
        text_node = TextNode("This is a test bold text", TextType.BOLD)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a test bold text")

    def test_bold_html_node_building(self):
        text_node = TextNode("This is a test bold text", TextType.BOLD)
        html_node = text_node_to_html_node(text_node).to_html()
        self.assertEqual(html_node, "<b>This is a test bold text</b>")

    def test_italic_html_node(self):
        text_node = TextNode("This is a test italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is a test italic text")

    def test_italic_html_node_building(self):
        text_node = TextNode("This is a test italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(text_node).to_html()
        self.assertEqual(html_node, "<i>This is a test italic text</i>")

    def test_code_html_node(self):
        text_node = TextNode("This is a test code", TextType.CODE)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a test code")

    def test_code_html_node_building(self):
        text_node = TextNode("This is a test code", TextType.CODE)
        html_node = text_node_to_html_node(text_node).to_html()
        self.assertEqual(html_node, "<code>This is a test code</code>")

    def test_link_html_node(self):
        text_node = TextNode("This is a test link", TextType.LINK)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a test link")

    def test_link_html_node_building(self):
        text_node = TextNode("This is a test link", TextType.LINK)
        html_node = text_node_to_html_node(text_node).to_html()
        self.assertEqual(html_node, "<a>This is a test link</a>")

    def test_image_html_node(self):
        text_node = TextNode("This is a test image", TextType.IMAGE)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")

    def test_image_html_node_building(self):
        text_node = TextNode(
            "This is a test image", TextType.IMAGE, url="www.google.com"
        )
        html_node = text_node_to_html_node(text_node).to_html()
        self.assertEqual(
            html_node, '<img src="www.google.com" alt="This is a test image"></img>'
        )


if __name__ == "__main__":
    unittest.main()
