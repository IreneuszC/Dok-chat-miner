import os
import sys

# For some reason __init__.py is not working
# TODO
# Fix absolute paths import within modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.paths import get_documents_path


class DocumentsReader:
    documents_directory = ""

    def __init__(self) -> None:
        self.documents_directory = get_documents_path()

    def get_files_to_process(self) -> list[dict]:
        result = []
        path = self.documents_directory

        for root, dirs, files in os.walk(path):
            folder_name = os.path.relpath(root, path)

            if folder_name == ".":
                continue

            files_without_summary = [
                f for f in files if f.endswith(".txt") and not f.endswith("summary.txt")
            ]

            if files_without_summary:
                result.append({"name": folder_name, "files": files_without_summary})

        return result

    def get_file_content(self, group_name: str, file_name: str) -> str:
        file_path = os.path.join(self.documents_directory, group_name, file_name)

        try:
            # ignore errors as some files has unknown not UTF-8 characters
            with open(file_path, "r", errors="ignore") as file:
                content = file.read()
            return content
        except FileNotFoundError:
            print(f"File '{file_path}' not found.")
            return ""
        except Exception as e:
            print(f"Error reading file '{file_path}': {e}")
            return ""

    def get_summary_files(self, group_name: str) -> list[str]:
        path = os.path.join(self.documents_directory, group_name)

        summary_files = []
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.endswith("_summary.txt"):
                    summary_files.append(os.path.join(root, file))
        return summary_files
