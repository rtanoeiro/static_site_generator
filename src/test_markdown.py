import unittest
from markdown_extract import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_bold_italic_code,
    split_nodes_image_link,
    text_to_textnodes,
)
from textnode import TextNode, TextType


class MarkdownExtractTests(unittest.TestCase):
    def test_extract_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        extracted_text = extract_markdown_images(text)
        self.assertEqual(
            extracted_text,
            [
                ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
            ],
        )

    def test_extract_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        extracted_text = extract_markdown_links(text)
        self.assertEqual(
            extracted_text,
            [
                ("to boot dev", "https://www.boot.dev"),
                ("to youtube", "https://www.youtube.com/@bootdotdev"),
            ],
        )

    def test_single_bold(self):
        node = TextNode("This is a bolded **word**", TextType.TEXT)
        new_nodes = split_nodes_bold_italic_code([node])
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is a bolded ", TextType.TEXT),
                TextNode("word", TextType.BOLD),
            ],
        )

    def test_only_bold(self):
        node = TextNode("**word**", TextType.TEXT)
        new_nodes = split_nodes_bold_italic_code([node])
        self.assertListEqual(
            new_nodes,
            [TextNode("word", TextType.BOLD)],
        )

    def test_single_italic(self):
        node = TextNode("This is a italic *word*", TextType.TEXT)
        new_nodes = split_nodes_bold_italic_code([node])
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is a italic ", TextType.TEXT),
                TextNode("word", TextType.ITALIC),
            ],
        )

    def test_only_italic(self):
        node = TextNode("*word*", TextType.TEXT)
        new_nodes = split_nodes_bold_italic_code([node])
        self.assertListEqual(
            new_nodes,
            [TextNode("word", TextType.ITALIC)],
        )

    def test_single_code(self):
        node = TextNode("This is a coded `word`", TextType.TEXT)
        new_nodes = split_nodes_bold_italic_code([node])
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is a coded ", TextType.TEXT),
                TextNode("word", TextType.CODE),
            ],
        )

    def test_only_code(self):
        node = TextNode("`word`", TextType.TEXT)
        new_nodes = split_nodes_bold_italic_code([node])
        self.assertListEqual(
            new_nodes,
            [TextNode("word", TextType.CODE)],
        )

    def test_multiple_bold(self):
        node = TextNode(
            "This is a bolded **word** and here another **bolded word**", TextType.TEXT
        )
        new_nodes = split_nodes_bold_italic_code([node])
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is a bolded ", TextType.TEXT),
                TextNode("word", TextType.BOLD),
                TextNode(" and here another ", TextType.TEXT),
                TextNode("bolded word", TextType.BOLD),
            ],
        )

    def test_multiple_italic(self):
        node = TextNode(
            "This is a italic *word* and here another *italic word*", TextType.TEXT
        )
        new_nodes = split_nodes_bold_italic_code([node])
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is a italic ", TextType.TEXT),
                TextNode("word", TextType.ITALIC),
                TextNode(" and here another ", TextType.TEXT),
                TextNode("italic word", TextType.ITALIC),
            ],
        )

    def test_multiple_code(self):
        node = TextNode(
            "This is a coded `word` and here another `coded word`", TextType.TEXT
        )
        new_nodes = split_nodes_bold_italic_code([node])
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is a coded ", TextType.TEXT),
                TextNode("word", TextType.CODE),
                TextNode(" and here another ", TextType.TEXT),
                TextNode("coded word", TextType.CODE),
            ],
        )

    def test_split_image_single(self):
        node = TextNode(
            "![image](https://www.example.com/image.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image_link([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://www.example.com/image.png"),
            ],
            new_nodes,
        )

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_link_single(self):
        node = TextNode(
            "This is my [link](https://www.example.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image_link([node])
        self.assertListEqual(
            [
                TextNode("This is my ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.example.com"),
            ],
            new_nodes,
        )

    def test_split_only_link(self):
        node = TextNode(
            "[link](https://www.example.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image_link([node])
        self.assertListEqual(
            [TextNode("link", TextType.LINK, "https://www.example.com")],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is my [link](https://www.example.com), hey, and this is [another link](https://www.example2.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image_link([node])
        self.assertListEqual(
            [
                TextNode("This is my ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.example.com"),
                TextNode(", hey, and this is ", TextType.TEXT),
                TextNode("another link", TextType.LINK, "https://www.example2.com"),
            ],
            new_nodes,
        )

    def test_multiple_markdown(self):
        text = "This is *italic* word with a **text** and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word with a ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode(
                "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
            ),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]

        self.assertEqual(new_nodes, expected)

    def test_another_multiple_markdown(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode(
                "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
            ),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertEqual(new_nodes, expected)


if __name__ == "__main__":
    unittest.main()
