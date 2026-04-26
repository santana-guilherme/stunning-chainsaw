import logging
import os
import shutil
from pathlib import Path

from src.md2html import markdown_to_html_node

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())
logger.setLevel(logging.INFO)

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
ch.setFormatter(formatter)
logger.addHandler(ch)


def copy_content(src: str, dest: str):
    # delete content on destination directory
    if os.path.exists(Path(dest).resolve()):
        shutil.rmtree(dest)
    os.mkdir(dest)
    # copy all content
    _recursive_copy(src, dest)


def _get_destination_path(src: str, dest: str):
    """
    Given a src concatenate the destination/src_subfolder(or files) without src top folder.
    Example:
        src: folder1/folder2
        dest: folder3
        produces: folder3/folder2
    """
    origin = src.split("/", maxsplit=1)[-1] if len(src.split("/")) > 1 else ""
    return os.path.join(Path(dest).resolve(), origin)


def _recursive_copy(current_path: str, dest: str):

    for el in os.listdir(current_path):
        # if its a file copy over to the dest
        if os.path.isfile(os.path.join(current_path, el)):
            # if the path to the files doesn't exists create it
            destination_path = _get_destination_path(current_path, dest)
            if not os.path.exists(destination_path):
                logger.info(
                    f"creating destination path: {destination_path} from current path {current_path}"
                )
                os.mkdir(destination_path)
            logger.info(
                f"Copying {os.path.join(current_path, el)} to {destination_path}"
            )
            shutil.copy(
                os.path.join(current_path, el),
                destination_path,
            )
        else:
            next_current_path = os.path.join(current_path, el)
            logger.info(f"recursive call on {next_current_path}")

            destination_path = _get_destination_path(next_current_path, dest)
            logger.info(
                f"use the opportunity to create the directory on the destination: {destination_path}"
            )
            os.mkdir(destination_path)
            # downside is that if we have a bunch of folders without a file we will create them for nothing
            _recursive_copy(next_current_path, dest)


def extract_title(markdown: str):
    splited = markdown.split("# ", maxsplit=2)
    if len(splited) < 2:
        raise Exception("No header on the text")

    # the title ends when we see a line break
    # we strip just for the sake of it
    return splited[1].split("\n")[0].strip()


def generate_page(from_path: str, template_path: str, dest_path: str, base_path: str):
    logger.info(
        f"Generating page from {from_path} to {dest_path} using {template_path}"
    )

    with open(from_path, "r") as f:
        markdown = f.read()

    with open(template_path, "r") as f:
        template = f.read()

    html_str = markdown_to_html_node(markdown).to_html()
    extracted_title = extract_title(markdown)

    template = template.replace("{{ Title }}", extracted_title).replace(
        "{{ Content }}", html_str
    )
    # update basepath
    if base_path != "/":
        template = template.replace('href="/', f'href="{base_path}').replace(
            'src="/', f'src="{base_path}'
        )

    dest_path_folders = dest_path.rsplit("/", maxsplit=1)[0]
    if not os.path.exists(dest_path_folders):
        os.makedirs(dest_path_folders)

    with open(os.path.join(dest_path), "w+") as f:
        f.write(template)


def generate_pages_recursive(
    dir_path_content: str, template_path: str, dest_dir_path: str, base_path: str
):
    for el in os.listdir(dir_path_content):
        current_el_path = os.path.join(dir_path_content, el)
        dest_el_path = os.path.join(dest_dir_path, el)
        if os.path.isfile(current_el_path):
            if el.endswith(".md"):
                dest_el_path = dest_el_path.replace(".md", ".html")
                generate_page(
                    from_path=current_el_path,
                    dest_path=dest_el_path,
                    template_path=template_path,
                    base_path=base_path,
                )
        else:
            generate_pages_recursive(
                dir_path_content=current_el_path,
                template_path=template_path,
                dest_dir_path=dest_el_path,
                base_path=base_path,
            )
