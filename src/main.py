from textnode import TextType, TextNode
from utility import *
import os
import shutil
STATIC_PATH = "./static"
PUBLIC_PATH = "./public"

def copy_directory_to_public(src_dir, dest_dir):
    if not os.path.exists(src_dir):
        return

    directory_items = os.listdir(src_dir)
    os.mkdir(dest_dir)
    for  item in directory_items:
        src_path = os.path.join(src_dir, item)
        dest_path = os.path.join(dest_dir, item)
        print(f"Copying {src_path}")
        if os.path.isfile(src_path):
            if os.path.exists(dest_path):
                os.remove(dest_path)
            shutil.copy(src_path, dest_path)
        else:
            copy_directory_to_public(src_path, dest_path)

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    md = ""
    template = ""

    with open(from_path, "r") as f:
        md = f.read()
    
    with open(template_path, "r") as f:
        template = f.read()
    
    title = extract_title(md)
    content = markdown_to_html_node(md).to_html()
    html = template.replace("{{ Title }}", title).replace("{{ Content }}", content)

    with open(dest_path, "w") as f:
        f.write(html)
    
    
    
    
    

def main():
    # text_node = TextNode("This is some anchor text", TextType.LINK, "https//www.boot.dev")
    # print(TextNode("Hello World", TextType.NORMAL))
    # print(text_node)
    if os.path.exists(PUBLIC_PATH): # Delete the entire public directory
        shutil.rmtree(PUBLIC_PATH)

    copy_directory_to_public(STATIC_PATH, PUBLIC_PATH) # Copy static data into the public directory
    generate_page("./content/index.md", "./template.html", "./public/index.html")

if __name__ == "__main__":
    main()
