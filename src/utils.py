import logging
import os
import shutil
from pathlib import Path

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
    # abs_src = str(pathlib.Path(src).resolve())
    # abs_dest = str(pathlib.Path(dest).resolve())
    _recursive_copy(src, dest)

def _get_destination_path(src: str, dest: str):
    """
    Given a src concatenate the destination/src_subfolder(or files) without src top folder.
    Example:
        src: folder1/folder2
        dest: folder3
        produces: folder3/folder2
    """
    origin = src.split('/', maxsplit=1)[-1] if len(src.split('/')) > 1 else ""
    return os.path.join(Path(dest).resolve(), origin)


def _recursive_copy(current_path: str, dest: str):

    for el in os.listdir(current_path):
        # if its a file copy over to the dest
        if os.path.isfile(os.path.join(current_path, el)):
            # if the path to the files doesn't exists create it
            destination_path = _get_destination_path(current_path, dest)
            if not os.path.exists(destination_path):
                logger.info(f"creating destination path: {destination_path} from current path {current_path}")
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
            logger.info(f"use the opportunity to create the directory on the destination: {destination_path}")
            os.mkdir(destination_path)
            # downside is that if we have a bunch of folders without a file we will create them for nothing
            _recursive_copy(next_current_path, dest)
