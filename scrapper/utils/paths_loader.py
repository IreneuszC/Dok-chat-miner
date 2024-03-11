class PathsLoader:
    def load_paths(self, file_path):
        paths = []
        with open(file_path) as file:
            for line in file:
                print(line.rstrip())
                paths.append(line.rstrip())
        return paths
