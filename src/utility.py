from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, TextType
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
    return re.findall(r"[^!]\[(.*?)\]\((.*?)\)", text)

if __name__ == "__main__":
    split_nodes_delimiter([TextNode("This is a text with a `code block` word", TextType.ITALIC)], "`", TextType.CODE)
    split_nodes_delimiter(["This is a text with a `code block`"], "`", TextType.CODE)
    split_nodes_delimiter(["This is a text with a without a code block word"], "`", TextType.CODE)
    split_nodes_delimiter(["This is a text with a `code block` word and another `code block`"], "`", TextType.CODE)
    split_nodes_delimiter(["This is a text with a `code block``code block`"], "`", TextType.CODE)