from textnode import TextType, TextNode
from utility import *
import os
import shutil
import sys
STATIC_PATH = "./static"
PUBLISH_PATH = "./docs"
TEMPLATE_PATH = "./template.html"
CONTENT_PATH = "./content"

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

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    md = ""
    template = ""

    with open(from_path, "r") as f:
        md = f.read()
    
    with open(template_path, "r") as f:
        template = f.read()
    
    title = extract_title(md)
    content = markdown_to_html_node(md).to_html()
    html = template.replace("{{ Title }}", title).replace("{{ Content }}", content).replace('href="/', f'href="{basepath}').replace('src="/', f'src="{basepath}')

    with open(dest_path, "w") as f:
        f.write(html)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    md_files = get_markdown_files(dir_path_content)
    for src_file in md_files:
        dest_folder = os.path.dirname(src_file).replace(dir_path_content, dest_dir_path)
        if not os.path.exists(dest_folder):
            os.makedirs(dest_folder)
        dest_file = os.path.join(dest_folder, os.path.basename(os.path.splitext(src_file)[0]) + ".html")
        generate_page(src_file, template_path, dest_file, basepath)
    
def get_markdown_files(dir_path):
    md_files = []
    directory_contents = os.listdir(dir_path)
    for item in directory_contents:
        fullPath = os.path.join(dir_path, item)
        if os.path.isdir(fullPath):
            md_files += get_markdown_files(fullPath)
        elif os.path.splitext(fullPath)[1].lower() == ".md":
            md_files.append(fullPath)
    return md_files
            
    
    
    

def main():
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    else:
        basepath = "/"

    if os.path.exists(PUBLISH_PATH): # Delete the entire public directory
        shutil.rmtree(PUBLISH_PATH)

    copy_directory_to_public(STATIC_PATH, PUBLISH_PATH) # Copy static data into the public directory
    #generate_page("./content/index.md", "./template.html", "./public/index.html")
    generate_pages_recursive(CONTENT_PATH, TEMPLATE_PATH, PUBLISH_PATH, basepath)

if __name__ == "__main__":
    main()
