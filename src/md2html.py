import re
from typing import List

from src.block_parser import BlockType, block_to_type, markdown_to_blocks
from src.inline_parser import (
    TextNode,
    TextType,
    text_node_to_html_node,
    text_to_textnodes,
)
from src.models.htmlnode import HTMLNode, LeafNode, ParentNode


def markdown_to_html_node(markdown: str):
    blocks: List[str] = markdown_to_blocks(markdown)

    parent_most_node = ParentNode(tag="div", children=[])
    for block in blocks:
        block_type = block_to_type(block)
        if block_type == BlockType.UNORDERED_LIST:
            children = [
                child.strip() for child in block.split("- ") if child.strip() != ""
            ]
            children = [
                ParentNode(tag="li", children=text_to_children(child))
                for child in children
            ]
            parent_most_node.children.append(ParentNode(tag="ul", children=children))
        elif block_type == BlockType.ORDERED_LIST:
            children = [
                child.strip()
                for child in re.split(r"\d. ", block)
                if child.strip() != ""
            ]
            children = [
                ParentNode(tag="li", children=text_to_children(child))
                for child in children
            ]
            parent_most_node.children.append(ParentNode(tag="ol", children=children))
        elif block_type == BlockType.PARAGRAPH:
            parent_most_node.children.append(
                ParentNode(tag="p", children=text_to_children(block))
            )
        elif block_type == BlockType.CODE:
            block = block.split("\n")
            block = "\n".join(block[1:-1]) + "\n"
            node = TextNode(text=block, text_type=TextType.CODE)
            node = text_node_to_html_node(node)
            parent = ParentNode(tag="pre", children=[node])
            parent_most_node.children.append(parent)
        elif block_type == BlockType.HEADING:
            title_size = block.count("#")
            parent_most_node.children.append(
                ParentNode(
                    tag=f"h{title_size}",
                    children=text_to_children(block.lstrip("#").strip()),
                )
            )
        elif block_type == BlockType.QUOTE:
            children = [
                child.strip() for child in block.split(">") if child.strip() != ""
            ]
            parent_most_node.children.append(
                ParentNode(
                    tag="blockquote", children=text_to_children("\n".join(children))
                )
            )
        else:
            parent_most_node.children.extend(text_to_children(block))
    return parent_most_node


def text_to_children(text: str) -> List[HTMLNode]:
    # Receive a text and return HTMLNodes list
    result: List[HTMLNode] = []
    text_nodes = text_to_textnodes(text)
    for node in text_nodes:
        result.append(text_node_to_html_node(node))
    return result
