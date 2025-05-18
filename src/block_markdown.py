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
        case block if re.match("`{3}(?s:.)*`{3}", block) != None: #(?s:.), re.DOTALL
            return BlockType.CODE
        case block if all_lines_match(block, "^>.*"):
            return BlockType.QUOTE
        case block if all_lines_match(block, "^-.*"):
            return BlockType.UNORDERED_LIST
        case block if is_ordered_list(block):
            return BlockType.ORDERED_LIST
        case _:
            return BlockType.PARAGRAPH

def all_lines_match(block, pattern):
    lineResults = [re.match(pattern, line) for line in block.splitlines()]
    return all(lineResults)

def is_ordered_list(block):
    lines = block.splitlines()
    for i in range(0, len(lines)):
        if re.match(rf"^{i + 1}\. .*", lines[i]) is None:
            return False
    return True
    

if __name__ == "__main__":
    text = """
# This is a heading


This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

- This is the first list item in a list block
- This is a list item
- This is another list item
    """
    print(block_to_block_type("####### This is a heading"))
