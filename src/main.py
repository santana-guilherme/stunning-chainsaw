from src.utils import copy_content, generate_page, generate_pages_recursive


def main():
    copy_content("static", "public")

    # generate_page("content/index.md", "template.html", "public/index.html")
    generate_pages_recursive("content", "template.html", "public")


main()
