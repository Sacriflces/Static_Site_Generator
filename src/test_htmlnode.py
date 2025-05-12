import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode
class TestHTMLNode(unittest.TestCase):
    
    def test_properties_default_to_none(self):
        sut = HTMLNode()
        expected_string_rep = "HTMLNode(None, None, "", None)"
        self.assertEqual(str(sut), expected_string_rep)
    
    def test_props_to_correct_html_representation(self):
        sut = HTMLNode("a", "boot.dev", None, {"href": "https://www.boot.dev", "target": "_blank"})
        expected_string_rep = ' href="https://www.boot.dev" target="_blank"'
        self.assertEqual(sut.props_to_html(), expected_string_rep)
    
    def test_to_html_not_implemented(self):
        sut = HTMLNode()
        self.assertRaises(NotImplementedError, sut.to_html)

class TestLeafNode(unittest.TestCase):

    def test_none_value_raises_exception(self):
        sut = LeafNode("p", None, None)
        self.assertRaises(ValueError, sut.to_html)
    
    def test_correct_html_rep_with_no_props(self):
        sut = LeafNode("p", "This is a paragraph of text.")
        expected_string_rep = "<p>This is a paragraph of text.</p>"
        self.assertEqual(sut.to_html(), expected_string_rep)

    def test_correct_html_rep_with_props(self):
        sut = LeafNode("a", "Click me!", {"href": "https://www.google.com", "target": "_blank"})
        expected_string_rep = '<a href="https://www.google.com" target="_blank">Click me!</a>'
        self.assertEqual(sut.to_html(), expected_string_rep)
    
    def test_leaf_to_html_no_tag(self):
        sut = LeafNode(None, "Hello, world!")
        self.assertEqual(sut.to_html(), "Hello, world!")

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        sut = ParentNode("div", [child_node])
        self.assertEqual(sut.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        sut = ParentNode("div", [child_node])
        self.assertEqual(
            sut.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    
    def test_no_children_raises_exception(self):
        sut = ParentNode("div", None)
        self.assertRaises(ValueError, sut.to_html)
    
    def test_zero_children_raises_exception(self):
        sut = ParentNode("div", [])
        self.assertRaises(ValueError, sut.to_html)
    
    def test_no_tag_raises_exception(self):
        child_node = LeafNode("b", "grandchild")
        sut = ParentNode(None,[child_node])
        self.assertRaises(ValueError, sut.to_html)
    
    def test_empty_tag_raises_exception(self):
        child_node = LeafNode("b", "grandchild")
        sut = ParentNode("",[child_node])
        self.assertRaises(ValueError, sut.to_html)

    def test_correct_html_rep_with_props(self):
        child_node = LeafNode("b", "Click me!")
        sut = ParentNode("a", [child_node], {"href": "https://www.google.com", "target": "_blank"})
        expected_string_rep = '<a href="https://www.google.com" target="_blank"><b>Click me!</b></a>'
        self.assertEqual(sut.to_html(), expected_string_rep)
    
    def test_correct_html_rep_with_multiple_children(self):
        children = [
            LeafNode("b", "child1"),
            LeafNode("i")
        ]
        
        
if __name__ == "__main__":
    unittest.main()