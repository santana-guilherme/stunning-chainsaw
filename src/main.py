from src.models.textnode import TextNode, TextType
from src.utils import copy_content

def main():
    a = TextNode("lala", TextType.LINK, "http://google.com")
    print(a)
    copy_content("static", "public")


main()
