import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_is_normal(self):
        node = TextNode("This is a text node", TextType.NORMAL)
        self.assertEqual(node.text_type, TextType.NORMAL)

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
        node = TextNode("This is a text node", TextType.IMAGES)
        self.assertEqual(node.text_type, TextType.IMAGES)

    def test_none_url(self):
        node = TextNode("This is a text node", TextType.NORMAL)
        self.assertEqual(node.url, None)

    def test_is_different(self):
        node = TextNode("This is a text node", TextType.NORMAL)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)


if __name__ == "__main__":
    unittest.main()
