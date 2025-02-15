import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_rep(self):
        props = {
            "href": "https://www.google.com",
            "target": "_blank",
        }
        node1 = HTMLNode("a", "this is a test", None, props)
        self.assertEqual(
            str(node1),
            """self.tag='a'\nself.value='this is a test'\nself.props={'href': 'https://www.google.com', 'target': '_blank'}\nself.children=None""",
        )

    def test_props_to_html(self):
        props = {
            "href": "https://www.google.com",
            "target": "_blank",
        }
        node1 = HTMLNode("a", "this is a test", None, props)
        self.assertEqual(
            node1.props_to_html(), ' href="https://www.google.com" target="_blank"'
        )


class TestLeafNode(unittest.TestCase):
    def test_to_html(self):
        props = {
            "href": "https://www.google.com",
            "target": "_blank",
        }
        node1 = LeafNode("a", "this is a test", props)
        self.assertEqual(
            node1.to_html(),
            '<a href="https://www.google.com" target="_blank">this is a test</a>',
        )


class TestParentNode(unittest.TestCase):
    def test_to_html(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )

        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_parent_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        node_out = ParentNode("link", [node, node, node])
        self.assertEqual(
            node_out.to_html(),
            "<link><p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p><p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p><p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p></link>",
        )


if __name__ == "__main__":
    unittest.main()
