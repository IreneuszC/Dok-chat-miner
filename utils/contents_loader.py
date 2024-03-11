class ContentsLoader:
    def load_contents(self, file_path):
        contents = []
        with open(file_path, encoding='UTF-8') as file:
            for line in file:
                line_text = line.rstrip()
                title = line_text.split(",")[0]
                content = line_text.split(",")[-1]
                contents.append({'content': content, 'title': title})
        return contents
