import unittest

from htmlnode import LeafNode, ParentNode
from markdown_documents import markdown_to_html_node


class TestMarkdownDocument(unittest.TestCase):
    def test_small(self):
        document = """# This is the **heading** and its **bold**

Here is some plain text with *italics*
"""
        expected_node = ParentNode(
            tag="div",
            children=[
                ParentNode(
                    tag="h1",
                    children=[
                        LeafNode(tag=None, value="This is the "),
                        LeafNode(tag="b", value="heading"),
                        LeafNode(tag=None, value=" and its "),
                        LeafNode(tag="b", value="bold"),
                    ],
                ),
                ParentNode(
                    tag="p",
                    children=[
                        LeafNode(tag=None, value="Here is some plain text with "),
                        LeafNode(tag="i", value="italics"),
                    ],
                ),
            ],
        )

        new_node = markdown_to_html_node(document)
        self.assertEqual(new_node.to_html(), expected_node.to_html())

    def test_code(self):
        return
        text = """```Check out the example
    code block here
neet **huh?**```"""
        expected_node = ParentNode(
            tag="div",
            children=[
                ParentNode(
                    tag="pre",
                    children=[
                        ParentNode(
                            tag="code",
                            children=[
                                LeafNode(
                                    tag=None,
                                    value="Check out the example\n    code block here\nneet ",
                                ),
                                LeafNode(tag="b", value="huh?"),
                            ],
                        )
                    ],
                )
            ],
        )
        new_node = markdown_to_html_node(text)
        self.assertEqual(new_node.to_html(), expected_node.to_html())

    def test_paragraph(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph\ntext in a p\ntag here</p></div>",
        )

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with *italic* text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph\ntext in a p\ntag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_lists(self):
        md = """
- This is a list
- with items
- and *more* items

1. This is an `ordered` list
2. with items
3. and more items

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
        )

    def test_headings(self):
        md = """
# this is an h1

this is paragraph text

## this is an h2
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",
        )

    def test_blockquote(self):
        md = """
> This is a
> blockquote block

this is paragraph text

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a\nblockquote block</blockquote><p>this is paragraph text</p></div>",
        )


if __name__ == "__main__":
    unittest.main()
