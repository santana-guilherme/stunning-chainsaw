import re
from enum import Enum
from typing import List


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_type(block: str) -> BlockType:
    block_type = BlockType.PARAGRAPH
    if re.search(r"^#{1,6} \w+", block):
        block_type = BlockType.HEADING
    elif block.startswith("```\n") and block.endswith("```"):
        block_type = BlockType.CODE
    elif re.search(r"^> ?.", block):
        block_type = BlockType.QUOTE
    elif block.startswith("- "):
        block_type = BlockType.UNORDERED_LIST
    elif re.search(r"^\d\. ", block):
        block_type = BlockType.ORDERED_LIST

    return block_type


def markdown_to_blocks(markdown: str) -> List[str]:
    return [block.strip() for block in markdown.split("\n\n") if block.strip() != ""]
