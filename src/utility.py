from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, TextType
from block_markdown import BlockType, markdown_to_blocks, block_to_block_type
import re
def text_node_to_html_node(text_node):
    htmlNode = None
    match text_node.text_type:
        case TextType.TEXT:
            htmlNode = LeafNode(None, text_node.text)
        case TextType.BOLD:
            htmlNode = LeafNode("b", text_node.text)
        case TextType.ITALIC:
            htmlNode = LeafNode("i", text_node.text)
        case TextType.CODE:
            htmlNode = LeafNode("code", text_node.text)
        case TextType.LINK:
            htmlNode = LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            htmlNode = LeafNode("img", None, {"src": text_node.url, "alt": text_node.text})

    return htmlNode

def split_nodes_delimiter(old_nodes, delimiter, textType):
    new_nodes = []
    for node in old_nodes:
        new_nodes_text = node.text.split(delimiter)
        if (len(new_nodes_text) == 1):
            new_nodes.append(node)
            continue
        for index in range(0, len(new_nodes_text)):
            if new_nodes_text[index] == "":
                continue
            new_nodes.append(TextNode(new_nodes_text[index], textType if index % 2 == 1 else node.text_type))
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        new_nodes_text = re.split(r"(!\[.*?\]\(.*?\))", node.text)
        if (len(new_nodes_text) == 1):
            new_nodes.append(node)
            continue
        for index in range(0, len(new_nodes_text)):
            if new_nodes_text[index] == "":
                continue
            if index % 2 == 1:
                alt_text, url = extract_markdown_images(new_nodes_text[index])[0]
                new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))
            else:
                new_nodes.append(TextNode(new_nodes_text[index], node.text_type))                
    return new_nodes

def split_nodes_link(old_nodes):
        new_nodes = []
        for node in old_nodes:
            new_nodes_text = re.split(r"(?<!!)(\[.*?\]\(.*?\))", node.text)
            if (len(new_nodes_text) == 1):
                new_nodes.append(node)
                continue
            for index in range(0, len(new_nodes_text)):
                if new_nodes_text[index] == "":
                    continue
                if index % 2 == 1:
                    alt_text, url = extract_markdown_links(new_nodes_text[index])[0]
                    new_nodes.append(TextNode(alt_text, TextType.LINK, url))
                else:
                    new_nodes.append(TextNode(new_nodes_text[index], node.text_type))                
        return new_nodes

def text_to_textnodes(text):
    startNode = TextNode(text, TextType.TEXT)
    return split_nodes_image(split_nodes_link((split_nodes_delimiter(split_nodes_delimiter(split_nodes_delimiter( [startNode], "**", TextType.BOLD), "_", TextType.ITALIC),"`", TextType.CODE))))

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    child_Nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        child = None
        match block_type: #Where we create the HTML Node
            case BlockType.HEADING:
                child = create_HTML_heading_node(block)
            case BlockType.CODE:
                child = create_HTML_code_node(block)
            case BlockType.QUOTE:
                child = create_HTML_blockquote_node(block)
            case BlockType.UNORDERED_LIST:
                child = create_HTML_unordered_list(block)
            case BlockType.ORDERED_LIST:
                child = create_HTML_ordered_list(block)
            case BlockType.PARAGRAPH:
                child = create_HTML_p_node(block)
        child_Nodes.append(child)
    return ParentNode("div", child_Nodes)


def create_HTML_heading_node(text):
    match = re.match("(#{1,6}) (.*)", text)
    tag = f"h{len(match.group(1))}"
    children = text_to_HTML_children(match.group(2))
    return ParentNode(tag, children)

def create_HTML_code_node(text):
    formatted_text = text.replace("```", "").lstrip()
    child = LeafNode("code", formatted_text)
    return ParentNode("pre", [child])

def create_HTML_blockquote_node(text):
    formatted_lines = [line.replace(">","").strip() for line in text.splitlines()]
    formatted_text = " ".join(formatted_lines)
    children = text_to_HTML_children(formatted_text)
    return ParentNode("blockquote", children)

def create_HTML_unordered_list(text):
    formatted_lines = [line.replace("-", "").strip() for line in text.splitlines()]
    children = text_to_listitems(formatted_lines)
    return ParentNode("ul", children)

def create_HTML_ordered_list(text):
    formatted_lines = [line[line.find(" "):].strip() for line in text.splitlines()]
    children = text_to_listitems(formatted_lines)
    return ParentNode("ol", children)

def text_to_listitems(lines):
    list_items = [ParentNode("li", text_to_HTML_children(line)) for line in lines]    
    return list_items

def create_HTML_p_node(text):
    formatted_text = text.replace("\n", " ")
    children = text_to_HTML_children(formatted_text)
    return ParentNode("p", children)


def text_to_HTML_children(text):
    return [text_node_to_html_node(text_node) for text_node in text_to_textnodes(text)]



    

if __name__ == "__main__":
    split_nodes_delimiter([TextNode("This is a text with a `code block` word", TextType.ITALIC)], "`", TextType.CODE)
    split_nodes_delimiter(["This is a text with a `code block`"], "`", TextType.CODE)
    split_nodes_delimiter(["This is a text with a without a code block word"], "`", TextType.CODE)
    split_nodes_delimiter(["This is a text with a `code block` word and another `code block`"], "`", TextType.CODE)
    split_nodes_delimiter(["This is a text with a `code block``code block`"], "`", TextType.CODE)
#Add functionality to deal with embedded inline elements like **blah _aye_ **. Could do a split based on the first inline element that we find and recursive perform the split until we don't have any more inline elements. (Also allow escape characters).
# Probably need to make it so TextNodes can have multiple TextTypes.