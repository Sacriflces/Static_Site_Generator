import unittest
from block_markdown import markdown_to_blocks
class TestBlockMarkdown(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    
    def test_markdown_to_single_block(self):
        md = "This is a single paragraph with _italic_ inline."
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["This is a single paragraph with _italic_ inline."])

    def test_markdown_to_blocks_removes_extra_lines(self):
        md = """
#This is a heading




And a regular paragraph, separated by
multiple lines!!
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "#This is a heading",
                "And a regular paragraph, separated by\nmultiple lines!!"
            ])
