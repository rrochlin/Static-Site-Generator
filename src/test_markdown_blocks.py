import unittest

from markdown_blocks import BlockType, block_to_block_type


class TestBlockToBlock(unittest.TestCase):
    def test_ordered_list(self):
        text_block = """1. this is an ordered list
2. this is the second item
3. this is the third item"""
        self.assertEqual(block_to_block_type(text_block), BlockType.ORDERED_LIST.value)

    def test_unordered_list(self):
        text_block = """- this list
* is mixed
- and has no
- order"""
        self.assertEqual(
            block_to_block_type(text_block), BlockType.UNORDERED_LIST.value
        )

    def test_headers(self):
        h1 = "# this is H1"
        h2 = "## this is H2"
        h3 = "### this is H3"
        h4 = "#### this is H4"
        h5 = "##### this is H5"
        h6 = "###### this is H5"
        hE = "####### this is an error"
        self.assertEqual(block_to_block_type(h1), BlockType.HEADING.value)
        self.assertEqual(block_to_block_type(h2), BlockType.HEADING.value)
        self.assertEqual(block_to_block_type(h3), BlockType.HEADING.value)
        self.assertEqual(block_to_block_type(h4), BlockType.HEADING.value)
        self.assertEqual(block_to_block_type(h5), BlockType.HEADING.value)
        self.assertEqual(block_to_block_type(h6), BlockType.HEADING.value)
        self.assertEqual(block_to_block_type(hE), "Normal")

    def test_code(self):
        code = """```this is a valid
            code block contained between backticks like `
            it is terminated by 3 consecutive `'s```"""
        self.assertEqual(block_to_block_type(code), BlockType.CODE.value)
        invalid = """```this is not a valid code block``"""
        self.assertEqual(block_to_block_type(invalid), "Normal")

    def test_quote(self):
        quote = """> Here is a quote
> By me
> For this test"""
        invalid = quote + "\nthis ruins the quote"
        self.assertEqual(block_to_block_type(quote), BlockType.QUOTE.value)
        self.assertEqual(block_to_block_type(invalid), "Normal")
