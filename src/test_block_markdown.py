import unittest
from block_markdown import markdown_to_blocks, block_to_block_type,BlockType
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

    def test_paragraph_block_returns_paragraph_blocktype(self):
        text = "This is a simple pargraph. It also contains TWO, I repeat TWO sentences!"
        rtnType = block_to_block_type(text)
        self.assertEqual(rtnType, BlockType.PARAGRAPH)
    
    def test_heading_block_with_six_hashtags_returns_heading_blocktype(self):
        text = "###### This is a heading"  
        rtnType = block_to_block_type(text)
        self.assertEqual(rtnType, BlockType.HEADING)
    
    def test_heading_block_with_single_hashtags_returns_heading_blocktype(self):
        text = "# This is a heading"  
        rtnType = block_to_block_type(text)
        self.assertEqual(rtnType, BlockType.HEADING)
    
    def test_heading_block_with_seven_hashtags_returns_pargraph_blocktype(self):
        text = "####### This is a heading"  
        rtnType = block_to_block_type(text)
        self.assertEqual(rtnType, BlockType.PARAGRAPH)
    
    def test_heading_block_with_missing_space_returns_paragraph_blocktype(self):
        text = "####This is a heading"  
        rtnType = block_to_block_type(text)
        self.assertEqual(rtnType, BlockType.PARAGRAPH)
    
    def test_single_line_code_block_returns_code_blocktype(self):
        text = "```int temp = 0;```"
        rtnType = block_to_block_type(text)
        self.assertEqual(rtnType, BlockType.CODE)
    
    def test_multi_line_code_block_returns_code_blocktype(self):
        text = """```
int temp = 0;
double value = 20.0;
```
"""
        rtnType = block_to_block_type(text)
        self.assertEqual(rtnType, BlockType.CODE)
    
    def test_missing_start_quotes_returns_paragraph_blocktype(self):
        text = """
int temp = 0;
double value = 20.0;
```
"""
        rtnType = block_to_block_type(text)
        self.assertEqual(rtnType, BlockType.PARAGRAPH)

    def test_missing_end_quotes_returns_paragraph_blocktype(self):
        text = """```
int temp = 0;
double value = 20.0;
"""
        rtnType = block_to_block_type(text)
        self.assertEqual(rtnType, BlockType.PARAGRAPH)
    
    def test_2_backticks_returns_paragraph_blocktype(self):
        text = """``
int temp = 0;
double value = 20.0;
``
"""
        rtnType = block_to_block_type(text)
        self.assertEqual(rtnType, BlockType.PARAGRAPH)
    
    def test_quote_block_returns_quote_blocktype(self):
        text = """> This is a random quote.
> From yours truly,
> Inqindi!
> by JService
"""
        rtnType = block_to_block_type(text)
        self.assertEqual(rtnType, BlockType.QUOTE)
    
    def test_quote_block_missing_start_character_returns_paragraph_blocktype(self):
        text = """> This is a random quote.
> From yours truly,
Inqindi!
> by JService
"""
        rtnType = block_to_block_type(text)
        self.assertEqual(rtnType, BlockType.PARAGRAPH)
    
    def test_unordered_list_returns_unordered_list_blocktype(self):
        text = """- Shopping List
-Apples
- Oranges
-Tomatoes
"""
        rtnType = block_to_block_type(text)
        self.assertEqual(rtnType, BlockType.UNORDERED_LIST)
    
    def test_unordered_list_missing_start_character_returns_paragraph_blocktype(self):
        text = """- Shopping List
- Apples
Oranges
-Tomatoes
"""
        rtnType = block_to_block_type(text)
        self.assertEqual(rtnType, BlockType.PARAGRAPH)
    
    def test_ordered_list_returns_ordered_list_blocktype(self):
        text = """1. Dust everything
2. Clean surfaces
3. Clean Cabinets
4. Vacuum / sweep the floor.
5. Swifter / Mop the floor.
"""
        rtnType = block_to_block_type(text)
        self.assertEqual(rtnType, BlockType.ORDERED_LIST)
    
    def test_ordered_list_missing_dot_returns_paragraph_blocktype(self):
        text = """1. Dust everything
2. Clean surfaces
3 Clean Cabinets
4. Vacuum / sweep the floor.
5. Swifter / Mop the floor.
"""
        rtnType = block_to_block_type(text)
        self.assertEqual(rtnType, BlockType.PARAGRAPH)

    def test_ordered_list_replaced_dot_returns_paragraph_blocktype(self):
        text = """1. Dust everything
2. Clean surfaces
3. Clean Cabinets
4D Vacuum / sweep the floor.
5. Swifter / Mop the floor.
"""
        rtnType = block_to_block_type(text)
        self.assertEqual(rtnType, BlockType.PARAGRAPH)

    def test_ordered_list_missing_number_returns_paragraph_blocktype(self):
        text = """1. Dust everything
2. Clean surfaces
3. Clean Cabinets
Vacuum / sweep the floor.
5. Swifter / Mop the floor.
"""
        rtnType = block_to_block_type(text)
        self.assertEqual(rtnType, BlockType.PARAGRAPH)

    def test_ordered_list_missing_space_returns_paragraph_blocktype(self):
        text = """1. Dust everything
2.Clean surfaces
3. Clean Cabinets
4. Vacuum / sweep the floor.
5. Swifter / Mop the floor.
"""
        rtnType = block_to_block_type(text)
        self.assertEqual(rtnType, BlockType.PARAGRAPH)