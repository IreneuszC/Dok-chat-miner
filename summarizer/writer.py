class Writer:
    def __init__(self) -> None:
        pass

    def save_to_file(self, path, content):
        try:
            with open(path, "w") as file:
                file.write(content)
            print(f"Content saved to {path} successfully.")
        except Exception as e:
            print(f"Error saving content to {path}: {e}")
