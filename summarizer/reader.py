import os
import fitz  # PyMuPDF


class DocumentsReader:
    full_directory = "documents/full"
    summarized_directory = "documents/summarized"

    def __init__(self) -> None:
        pass

    def get_lowercase_filenames(self, directory) -> list[str]:
        return [os.path.splitext(file.lower())[0] for file in os.listdir(directory)]

    def read_pdf(self, file_path) -> str:
        doc = fitz.open(file_path)
        text = ""
        for page_num in range(doc.page_count):
            page = doc[page_num]
            text += page.get_text()  # type: ignore
        doc.close()
        return text

    def get_files_to_process(self) -> set[str]:
        full_files = set(self.get_lowercase_filenames(self.full_directory))
        summarized_files = set(self.get_lowercase_filenames(self.summarized_directory))

        return full_files - summarized_files

    def get_file_content(self, filename: str) -> str:
        file_path = os.path.join(self.full_directory, filename + ".pdf")

        return self.read_pdf(file_path)
