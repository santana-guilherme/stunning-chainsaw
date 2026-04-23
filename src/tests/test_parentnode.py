import unittest

from src.models.htmlnode import LeafNode, ParentNode


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_grandchildren_props(self):
        grandchild_node = LeafNode("b", "grandchild", {"id": "#la"})
        grandchild_node_2 = LeafNode("b", "grandchild2", {"id": "#la2"})
        child_node = ParentNode("span", [grandchild_node])
        child_node_2 = ParentNode("p", [grandchild_node_2])
        parent_node = ParentNode("div", [child_node, child_node_2], {"height": "152px"})
        self.assertEqual(
            parent_node.to_html(),
            '<div height="152px"><span><b id="#la">grandchild</b></span><p><b id="#la2">grandchild2</b></p></div>',
        )
