import unittest

from src.models.htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(
            "h1",
            "this is a title",
            props={"class": ".titles", "href": "http://google.com"},
        )
        self.assertEqual(
            node.props_to_html(), ' class=".titles" href="http://google.com"'
        )

    def test_props_to_html_2(self):
        node2 = HTMLNode(
            "img",
            props={"alt": "sr google", "src": "http://google.com/someimage.png"},
        )
        self.assertEqual(
            node2.props_to_html(),
            ' alt="sr google" src="http://google.com/someimage.png"',
        )

    def test_repr(self):
        node = HTMLNode(
            "h1",
            "this is a title",
            props={"class": ".titles", "href": "http://google.com"},
        )

        self.assertEqual(
            str(node),
            "HTMLNode(h1, this is a title, None, {'class': '.titles', 'href': 'http://google.com'})",
        )
