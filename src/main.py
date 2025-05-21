from textnode import TextType, TextNode
import os
import shutil
STATIC_PATH = "./static"
PUBLIC_PATH = "./public"
def copy_directory_to_public(src_dir, dest_dir):
    if not os.path.exists(src_dir):
        return
    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)

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
    

def main():
    # text_node = TextNode("This is some anchor text", TextType.LINK, "https//www.boot.dev")
    # print(TextNode("Hello World", TextType.NORMAL))
    # print(text_node)
    copy_directory_to_public(STATIC_PATH, PUBLIC_PATH)

if __name__ == "__main__":
    main()
