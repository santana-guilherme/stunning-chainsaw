import unittest

from src.block_parser import BlockType, block_to_type, markdown_to_blocks


class TestBlockParser(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_block_to_type(self):
        cases = [
            (">> Asdçlfkjasdklfjs", BlockType.PARAGRAPH),
            ("#### A heading", BlockType.HEADING),
            (
                """```
                some code
                ```""",
                BlockType.CODE,
            ),
            ("""> Quoting someone""", BlockType.QUOTE),
            (
                """- value one
                - value two
                """,
                BlockType.UNORDERED_LIST,
            ),
            (
                """1. value one
                2. value two
                """,
                BlockType.ORDERED_LIST,
            ),
        ]
        for block, expected_type in cases:
            self.assertEqual(block_to_type(block), expected_type)
