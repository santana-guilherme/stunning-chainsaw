import unittest

from src.inline_parser import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_node_to_html_node,
    text_to_textnodes,
)
from src.models.textnode import TextNode, TextType


class TestInlineParser(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_split_nodes_delimiter(self):
        cases = [
            (
                ("`", TextType.CODE),
                [
                    TextNode(
                        "This is text with a `code block` word. Also `this` one",
                        TextType.TEXT,
                    )
                ],
                [
                    TextNode("This is text with a ", TextType.TEXT),
                    TextNode("code block", TextType.CODE),
                    TextNode(" word. Also ", TextType.TEXT),
                    TextNode("this", TextType.CODE),
                    TextNode(" one", TextType.TEXT),
                ],
            ),
            (
                ("-", TextType.LIST_ITEM),
                [
                    TextNode(
                        "- A list item",
                        TextType.TEXT,
                    )
                ],
                [
                    TextNode(" A list item", TextType.LIST_ITEM),
                    # TextNode(" Another item", TextType.LIST_ITEM),
                ],
            ),
            (
                ("`", TextType.CODE),
                [
                    TextNode(
                        """
```
code block
```""",
                        TextType.TEXT,
                    )
                ],
                [TextNode(" code block ", TextType.CODE)],
            ),
            (
                (r"^\d\. ", TextType.LIST_ITEM, True),
                [
                    TextNode(
                        """1. this is a ordered list item""",
                        TextType.TEXT,
                    )
                ],
                [TextNode("this is a ordered list item", TextType.LIST_ITEM)],
            ),
        ]
        for args, nodes, expected in cases:
            new_nodes = split_nodes_delimiter(nodes, *args)
            self.assertEqual(new_nodes, expected)

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with an [link](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("link", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev) aha [to boot dev](https://www.boot.dev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode(
                    "to boot dev",
                    TextType.LINK,
                    "https://www.boot.dev",
                ),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
                TextNode(" aha ", TextType.TEXT),
                TextNode(
                    "to boot dev",
                    TextType.LINK,
                    "https://www.boot.dev",
                ),
            ],
        )

    def test_split_image(self):
        node = TextNode(
            "![img1](https://www.boot.dev) a ![img2](https://www.boot.dev) and ![img3](https://www.boot.dev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            new_nodes,
            [
                TextNode("img1", TextType.IMAGE, "https://www.boot.dev"),
                TextNode(" a ", TextType.TEXT),
                TextNode("img2", TextType.IMAGE, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("img3", TextType.IMAGE, "https://www.boot.dev"),
            ],
        )

        node = TextNode(
            "abc ![img1](https://www.boot.dev) def",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            new_nodes,
            [
                TextNode("abc ", TextType.TEXT),
                TextNode("img1", TextType.IMAGE, "https://www.boot.dev"),
                TextNode(" def", TextType.TEXT),
            ],
        )

    def test_text_to_textnodes(self):
        nodes = text_to_textnodes(
            """This is **text** with an _italic_ word and a `code block` and
            an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"""
        )
        self.assertEqual(
            nodes,
            [
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
            ],
        )
