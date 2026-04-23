from typing import List


class HTMLNode:
    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        children: List["HTMLNode"] | None = None,
        props: dict | None = None,
    ) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self) -> str:
        if not self.props:
            return ""
        return " " + " ".join([f'{k}="{v}"' for k, v in self.props.items()])

    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"


class LeafNode(HTMLNode):
    def __init__(
        self,
        tag: str | None,
        value: str,
        props: dict | None = None,
    ) -> None:
        super().__init__(tag, value, [], props)

    def to_html(self):
        if not self.value:
            raise ValueError("No value")
        if not self.tag:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value if self.value else ''}</{self.tag}>"

    def __repr__(self) -> str:
        return f"LeafNode({self.tag}, {self.value}, {self.props})"


class ParentNode(HTMLNode):
    def __init__(
        self,
        tag: str,
        children: List["HTMLNode"],
        props: dict | None = None,
    ) -> None:
        self.tag = tag
        self.children = children
        self.props = props

    def __repr__(self) -> str:
        return f"ParentNode({self.tag}, {self.children}, {self.props})"

    def to_html(self):
        if not self.tag:
            raise ValueError("No tag")
        if not self.children:
            raise ValueError("No children on ParentNode")

        children_html = []
        for child in self.children:
            children_html.append(child.to_html())
        children_html = "".join(children_html)
        return f"""<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"""
