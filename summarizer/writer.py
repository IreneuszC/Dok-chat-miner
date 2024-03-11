import os
import sys

# For some reason __init__.py is not working
# TODO
# Fix absolute paths import within modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.paths import get_documents_path


class Writer:
    documents_directory = ""

    def __init__(self) -> None:
        self.documents_directory = get_documents_path()

    def save_to_file(self, group_name: str, file_name: str, content: str):
        path = os.path.join(self.documents_directory, group_name, file_name)
        try:
            with open(path, "w") as file:
                file.write(content)
            print(f"Content saved to {path} successfully.")
        except Exception as e:
            print(f"Error saving content to {path}: {e}")
