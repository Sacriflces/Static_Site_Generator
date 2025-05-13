import unittest
from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
from utility import text_node_to_html_node, split_nodes_delimiter

class TestUtility(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        sut = text_node_to_html_node(node)
        expected_html = "This is a text node"
        self.assertEqual(sut.to_html(), expected_html)
    
    def test_bold(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        sut = text_node_to_html_node(node)
        expected_html = "<b>This is a bold node</b>"
        self.assertEqual(sut.to_html(), expected_html)


    def test_italic(self):
        node = TextNode("This is an italic node", TextType.ITALIC)
        sut = text_node_to_html_node(node)
        expected_html = "<i>This is an italic node</i>"
        self.assertEqual(sut.to_html(), expected_html)
    
    def test_code(self):
        node = TextNode("This is a code node", TextType.CODE)
        sut = text_node_to_html_node(node)
        expected_html = "<code>This is a code node</code>"
        self.assertEqual(sut.to_html(), expected_html)

    def test_link(self):
        node = TextNode("This is a link node", TextType.LINK, "https://example.com")
        sut = text_node_to_html_node(node)
        expected_html = '<a href="https://example.com">This is a link node</a>'
        self.assertEqual(sut.to_html(), expected_html)
    
    def test_image(self):
        node = TextNode("This is an image node", TextType.IMAGE, "https://example.com/image01")
        sut = text_node_to_html_node(node)
        expected_html = '<img "src=https://example.com/image01" alt="This is an image node"></img>'
    
    def test_split_node_single_nested_italic(self):
        nodes = [TextNode("This is a text with a `code block` word")]
        sut = split_nodes_delimiter(nodes, "`", TextType.Code)
        self.assertEqual(sut, [TextNode("This is a text with a ", TextNode.TEXT),
                               TextNode("code block", TextType.CODE),
                               TextNode(" word", TextType.TEXT)])
    

if __name__ == "__main__":
    unittest.main()