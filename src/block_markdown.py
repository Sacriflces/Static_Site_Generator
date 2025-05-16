from enum import Enum
import re

class BlockType(Enum):
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"
    PARAGRAPH = "paragraph"

def markdown_to_blocks(markdown):
    blocks = [line.strip() for line in markdown.split("\n\n") if not (line.isspace() or line == "")]
    return blocks

def block_to_block_type(block):
    match (block):
        case block if re.match("#{1,6} ", block) != None:
            return BlockType.HEADING
        case block if re.match("`{3}(?s:.)`{3}") != None:
            return BlockType.CODE
        case block if re.match("")
            

if __name__ == "__main__":
    text = """
# This is a heading


This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

- This is the first list item in a list block
- This is a list item
- This is another list item
    """
    print(block_to_block_type("####### This is a heading"))
