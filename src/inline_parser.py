import re
from typing import List

from src.models.htmlnode import LeafNode
from src.models.textnode import TextNode, TextType


def split_nodes_delimiter(
    old_nodes: List[TextNode], delimiter: str, text_type: TextType, regex: bool = False
):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        if regex:
            text_parts = re.split(delimiter, node.text)
        else:
            text_parts = node.text.split(delimiter)

        for idx, part in enumerate(text_parts, start=1):
            part = part.replace("\n", " ").replace("  ", " ")
            if part.strip() == "":
                continue
            new_node = TextNode(text=part, text_type=TextType.TEXT)
            # only even indexes should be interpreted as `text_type`
            if idx % 2 != 0:
                new_nodes.append(new_node)
                continue
            new_node.text = new_node.text
            new_node.text_type = text_type
            new_nodes.append(new_node)
    return new_nodes


def split_nodes_link(old_nodes: List[TextNode]) -> List[TextNode]:
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        matches = extract_markdown_links(old_node.text)
        if not matches:
            new_nodes.append(old_node)
            continue

        remain_text = old_node.text
        for match in matches:
            if not remain_text:
                break

            splits = remain_text.split(f"[{match[0]}]({match[1]})", maxsplit=1)

            if len(splits) == 1:
                # we didn't found value to split
                new_nodes.append(TextNode(text=splits[0], text_type=TextType.TEXT))
            else:
                if splits[0] != "":
                    new_nodes.append(TextNode(text=splits[0], text_type=TextType.TEXT))
                new_nodes.append(
                    TextNode(text=match[0], text_type=TextType.LINK, url=match[1])
                )
            remain_text = splits[-1]
        if remain_text and remain_text != "":
            new_nodes.append(TextNode(text=remain_text, text_type=TextType.TEXT))
    return new_nodes


def split_nodes_image(old_nodes: List[TextNode]):
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        matches = extract_markdown_images(old_node.text)
        if not matches:
            new_nodes.append(old_node)
            continue

        remain_text = old_node.text
        for match in matches:
            if not remain_text:
                break

            splits = remain_text.split(f"![{match[0]}]({match[1]})", maxsplit=1)

            if len(splits) == 1:
                # we didn't found value to split
                new_nodes.append(TextNode(text=splits[0], text_type=TextType.TEXT))
            else:
                if splits[0] != "":
                    new_nodes.append(TextNode(text=splits[0], text_type=TextType.TEXT))
                new_nodes.append(
                    TextNode(text=match[0], text_type=TextType.IMAGE, url=match[1])
                )
            remain_text = splits[-1]
        if remain_text and remain_text != "":
            new_nodes.append(TextNode(text=remain_text, text_type=TextType.TEXT))
    return new_nodes


def extract_markdown_images(text: str):
    return re.findall(r"!\[(.+?)\]\((.+?)\)", text)


def extract_markdown_links(text: str):
    return re.findall(r"(?<!!)\[(.+?)\]\((.+?)\)", text)


def text_to_textnodes(text: str) -> List[TextNode]:

    # transforma BOLD
    nodes = split_nodes_delimiter(
        old_nodes=[TextNode(text=text, text_type=TextType.TEXT)],
        delimiter="**",
        text_type=TextType.BOLD,
    )
    # transforma ITALIC
    nodes = split_nodes_delimiter(
        old_nodes=nodes,
        delimiter="_",
        text_type=TextType.ITALIC,
    )
    # transforma LIST ITEM
    # nodes = split_nodes_delimiter(
    #     old_nodes=nodes,
    #     delimiter="-",
    #     text_type=TextType.LIST_ITEM,
    # )
    # transforma CODE
    nodes = split_nodes_delimiter(
        old_nodes=nodes,
        delimiter="`",
        text_type=TextType.CODE,
    )
    # transforma QUOTE
    # nodes = split_nodes_delimiter(
    #     old_nodes=nodes, delimiter="> \w+\s", text_type=TextType.QUOTE, regex=True
    # )
    # transforma LINK
    nodes = split_nodes_link(old_nodes=nodes)
    # transforma IMAGE
    nodes = split_nodes_image(old_nodes=nodes)
    return nodes


def text_node_to_html_node(text_node: TextNode):
    if text_node.text_type not in TextType:
        raise Exception(f"Text type not valid for {text_node}")

    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(tag=None, value=text_node.text)
        case TextType.BOLD:
            return LeafNode(tag="b", value=text_node.text)
        case TextType.ITALIC:
            return LeafNode(tag="i", value=text_node.text)
        case TextType.CODE:
            return LeafNode(tag="code", value=text_node.text)
        case TextType.LIST_ITEM:
            return LeafNode(tag="li", value=text_node.text)
        case TextType.LINK:
            return LeafNode(
                tag="a", value=text_node.text, props={"href": text_node.url}
            )
        case TextType.IMAGE:
            return LeafNode(
                tag="img",
                value="",
                props={"src": text_node.url, "alt": text_node.text},
            )
        case TextType.QUOTE:
            return LeafNode(tag="blockquote", value=text_node.text)
        case _:
            raise Exception("We don't know what to do")
