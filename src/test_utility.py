import unittest
from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
from utility import text_node_to_html_node, split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes, markdown_to_html_node

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
    
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )
    
    def test_headings(self):
        md = """
# Heading 1

## Heading 2

### Heading 3

#### Heading 4

##### Heading 5

###### Heading 6
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Heading 1</h1><h2>Heading 2</h2><h3>Heading 3</h3><h4>Heading 4</h4><h5>Heading 5</h5><h6>Heading 6</h6></div>"
        )
    
    def test_headings_with_inline_elements(self):
        md = """
# _Heading_ 1

## **Heading** 2

### Heading 3

#### Heading 4

##### Heading 5

###### Heading 6
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1><i>Heading</i> 1</h1><h2><b>Heading</b> 2</h2><h3>Heading 3</h3><h4>Heading 4</h4><h5>Heading 5</h5><h6>Heading 6</h6></div>"
        )
    
    def test_quote(self):
        md = """> This is a random quote.
> From yours truly,
> Inqindi!
> by JService
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a random quote. From yours truly, Inqindi! by JService</blockquote></div>"
        )
    
    def test_quote_with_inline_elements(self):
        md = """> This is a _random_ quote.
> From **yours** truly,
> Inqindi!
> by JService
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a <i>random</i> quote. From <b>yours</b> truly, Inqindi! by JService</blockquote></div>"
        )
    
    def test_unordered_list(self):
        md = """- Shopping List
- Apples
- Oranges
- Tomatoes
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>Shopping List</li><li>Apples</li><li>Oranges</li><li>Tomatoes</li></ul></div>"
        )
    
    def test_unordered_list_with_inline_elements(self):
        md = """- _Shopping_ **Li**st
- _Apples_
- **Oranges**
- Tomatoes
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li><i>Shopping</i> <b>Li</b>st</li><li><i>Apples</i></li><li><b>Oranges</b></li><li>Tomatoes</li></ul></div>"
        )
    
    def test_ordered_list(self):
        md ="""1. Dust everything
2. Clean surfaces
3. Clean Cabinets
4. Vacuum / sweep the floor.
5. Swifter / Mop the floor.
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>Dust everything</li><li>Clean surfaces</li><li>Clean Cabinets</li><li>Vacuum / sweep the floor.</li><li>Swifter / Mop the floor.</li></ol></div>"
        )

    def test_ordered_list_with_inline_elements(self):
        md ="""1. _Dust_ everything
2. Clean surfaces
3. Clean **Cabinets**
4. Vacuum / `sweep the floor`.
5. Swifter / Mop the floor.
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li><i>Dust</i> everything</li><li>Clean surfaces</li><li>Clean <b>Cabinets</b></li><li>Vacuum / <code>sweep the floor</code>.</li><li>Swifter / Mop the floor.</li></ol></div>"
        )
    
    def test_markdown_with_multiple_blocks(self):
        md = """ # Software Engineer Job Posting Asks

## Number of Postings Reviewed: **10**

### Skills ranked by relevance

1. Cloud Platform
2. SQL Database
3. Python
4. C#
5. Javascript
6. Frontend Framework

### Additional Skills in no particular order

- Agile
- MySQL
- Git
- CI/CD
- C++

I reviewed job postings on [LinkedIn](https://linkedin.com) Also.. here's an image of ![Obi Wan](https://i.imgur.com/fJRm4Vk.jpeg)

The following is example of code in C++. It uses the `cout` object.

```
using namespace std;
cout << "Hello World!" << endl;
```

> I fear not the man who has practiced 10,000 kicks once,
> but I fear the man who has practiced one kick 10,000 times.
> by _Bruce Lee_
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><h1>Software Engineer Job Posting Asks</h1><h2>Number of Postings Reviewed: <b>10</b></h2><h3>Skills ranked by relevance</h3><ol><li>Cloud Platform</li><li>SQL Database</li><li>Python</li><li>C#</li><li>Javascript</li><li>Frontend Framework</li></ol><h3>AdditionalSkills in no particular order</h3><ul><li>Agile</li><li>MySQL</li><li>Git</li><li>CI/CD</li><li>C++</li></ul><p></p></div>")

if __name__ == "__main__":
    unittest.main()