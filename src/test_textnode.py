import unittest
from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    
    def test_two_nodes_different_text_property_not_equal(self):
        sut = TextNode("This is a text node", TextType.BOLD)
        node_cmp = TextNode("This is also a text node", TextType.BOLD)
        self.assertNotEqual(sut, node_cmp)

    def test_two_nodes_different_type_property_not_equal(self):
        sut = TextNode("This is a text node", TextType.BOLD)
        node_cmp = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(sut, node_cmp)

    def test_two_nodes_different_url_property_not_equal(self):
        sut = TextNode("This is a text node", TextType.IMAGE, "https://example.com/image1")
        node_cmp = TextNode("This is a text node", TextType.IMAGE, "https://example.com/image2")
        self.assertNotEqual(sut, node_cmp)

    def test_two_link_nodes_same_properties_equal(self):
        sut = TextNode("This is a text node", TextType.IMAGE, "https://example.com/image1")
        node_cmp = TextNode("This is a text node", TextType.IMAGE, "https://example.com/image1")
        self.assertEqual(sut, node_cmp)

    def test_non_url_node_correct_string_rep(self):
        sut = TextNode("Hello World!", TextType.NORMAL)
        text_rep = str(sut)
        expected = "TextNode(Hello World!, normal, None)"
        self.assertEqual(text_rep, expected)

    def test_url_node_correct_string_rep(self):
        sut = TextNode("This is some anchor text", TextType.LINK, "https//www.boot.dev")
        text_rep = str(sut)
        expected = "TextNode(This is some anchor text, link, https//www.boot.dev)"
        self.assertEqual(text_rep, expected)


if __name__ == "__main__":
    unittest.main()