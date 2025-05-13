import unittest
from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
from utility import text_node_to_html_node

class TestUtility(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        sut = text_node_to_html_node(node)
        self.assertEqual(sut.tag, None)
        self.assertEqual(sut.value, "This is a text node")