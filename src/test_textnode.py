import unittest

from htmlnode import LeafNode
from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_rep(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual("TextNode(This is a text node, bold, None)", str(node))

    def test_neq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)


class TestTextConversionFunction(unittest.TestCase):
    def test_bold(self):
        text_node = TextNode("this is a test node", TextType.BOLD)
        leaf_node = LeafNode(tag="b", value="this is a test node")
        self.assertEqual(text_node_to_html_node(text_node), leaf_node)

    def test_image(self):
        text_node = TextNode("this is alt text", TextType.IMAGES, "image.route")
        leaf_node = LeafNode(
            tag="img", value="", props={"src": "image.route", "alt": "this is alt text"}
        )
        self.assertEqual(text_node_to_html_node(text_node), leaf_node)


if __name__ == "__main__":
    unittest.main()
