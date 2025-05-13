from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, TextType

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
            
