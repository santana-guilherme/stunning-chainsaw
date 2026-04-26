import sys

from src.utils import copy_content, generate_pages_recursive


def main():

    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"

    copy_content("static", "docs")
    generate_pages_recursive(
        dir_path_content="content",
        template_path="template.html",
        dest_dir_path="docs",
        base_path=basepath,
    )


main()
