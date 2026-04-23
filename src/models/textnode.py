from enum import Enum


class TextType(Enum):
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"
    TEXT = "text"
    LIST_ITEM = "list_item"


class TextNode:
    """Inline text type"""

    def __init__(self, text: str, text_type: TextType, url: str | None = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, o: "TextNode"):
        return (
            self.text == o.text and self.text_type == o.text_type and self.url == o.url
        )

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
