import unittest
from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
from utility import text_node_to_html_node, split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes

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
    
    def test_split_node_single_nested_code(self):
        nodes = [TextNode("This is a text with a `code block` word", TextType.TEXT)]
        sut = split_nodes_delimiter(nodes, "`", TextType.CODE)
        self.assertEqual(sut, [TextNode("This is a text with a ", TextType.TEXT),
                               TextNode("code block", TextType.CODE),
                               TextNode(" word", TextType.TEXT)])
    
    def test_split_node_multiple_nested_code(self):
        nodes = [TextNode("This is a text with a `code block` word and another `code block`", TextType.TEXT)]
        sut = split_nodes_delimiter(nodes, "`", TextType.CODE)
        self.assertEqual(sut, [TextNode("This is a text with a ", TextType.TEXT),
                               TextNode("code block", TextType.CODE),
                               TextNode(" word and another ", TextType.TEXT),
                               TextNode("code block", TextType.CODE)])
    
    def test_split_node_multiple_TextNodes_with_nested_code(self):
        nodes = [TextNode("This is a text with a `code block` word and another `code block` Okay", TextType.TEXT),
                TextNode("Hello World!", TextType.TEXT),
                TextNode("`String temp = String.Empty`", TextType.TEXT)]
        sut = split_nodes_delimiter(nodes, "`", TextType.CODE)
        self.assertEqual(sut, [TextNode("This is a text with a ", TextType.TEXT),
                               TextNode("code block", TextType.CODE),
                               TextNode(" word and another ", TextType.TEXT),
                               TextNode("code block", TextType.CODE),
                               TextNode(" Okay", TextType.TEXT),
                               TextNode("Hello World!", TextType.TEXT),
                               TextNode("String temp = String.Empty", TextType.CODE)])
    
    def test_split_node_multiple_nested_bold(self):
        nodes = [TextNode("This contains multiple **bold** text **nodes**!", TextType.TEXT)]
        sut = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertEqual(sut, [TextNode("This contains multiple ", TextType.TEXT),
                               TextNode("bold", TextType.BOLD),
                               TextNode(" text ", TextType.TEXT),
                               TextNode("nodes", TextType.BOLD),
                               TextNode("!", TextType.TEXT)])
    
    def test_split_node_multiple_nested_italic(self):
        nodes = [TextNode("This contains multiple _italic_ text _nodes_!", TextType.TEXT)]
        sut = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
        self.assertEqual(sut, [TextNode("This contains multiple ", TextType.TEXT),
                               TextNode("italic", TextType.ITALIC),
                               TextNode(" text ", TextType.TEXT),
                               TextNode("nodes", TextType.ITALIC),
                               TextNode("!", TextType.TEXT)])
    
    def test_split_node_nested_inline_elements(self):
        nodes = [TextNode("This is an _italic and **bold** word_.", TextType.TEXT)]
        sut = split_nodes_delimiter(split_nodes_delimiter(nodes, "_", TextType.ITALIC), "**", TextType.BOLD)
        self.assertEqual(sut, [TextNode("This is an ", TextType.TEXT),
                               TextNode("italic and ", TextType.ITALIC),
                               TextNode("bold", TextType.BOLD),
                               TextNode(" word", TextType.ITALIC),
                               TextNode(".", TextType.TEXT)])
    
    def test_extract_markdown_images(self):
        sut = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], sut)
    
    def test_extract_markdown_multiple_images(self):
        sut = extract_markdown_images(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        )
        self.assertListEqual([("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                              ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg" )], sut)
    
    def test_extract_markdown_multiple_links(self):
        sut = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev"),
                              ("to youtube", "https://www.youtube.com/@bootdotdev")], sut)
    
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        sut = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            sut)
    
    def test_split_links(self):
        node = TextNode(
            "This is text with an [link](https://humblebundle.com) and another [second link](https://www.google.com)",
            TextType.TEXT,
        )
        sut = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://humblebundle.com"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://www.google.com"
                ),
            ],
            sut)
    
    def test_single_image(self):
        node = TextNode("![image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT)
        sut = split_nodes_image([node])
        self.assertListEqual(
            [TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png")],
            sut)
        
    def test_single_link(self):
        node = TextNode("[link](https://humblebundle.com)", TextType.TEXT)
        sut = split_nodes_link([node])
        self.assertListEqual(
            [TextNode("link", TextType.LINK, "https://humblebundle.com"),],
            sut)

    def test_image_not_a_link(self):
        node = TextNode("![image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT)
        sut = split_nodes_link([node])
        self.assertListEqual(
            [TextNode("![image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT)],
            sut)
        
    def test_link_not_a_link(self):
        node = TextNode("[link](https://humblebundle.com)", TextType.TEXT)
        sut = split_nodes_image([node])
        self.assertListEqual(
            [TextNode("[link](https://humblebundle.com)", TextType.TEXT)],
            sut)
    
    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        sut = text_to_textnodes(text)
        self.assertListEqual([
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),], sut)
        
if __name__ == "__main__":
    unittest.main()