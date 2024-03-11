import os

ARTICLES_PATH = "output/CisaGovUscertIcsAdvisoriesContentSpider/content_cleaned.txt"
SAVE_PATH = "output/clustering_results"


# labels: [1 2 1 1 0 0 0 0 0 0]
# dict: {
# "ethernet": [1],
# "government": [0],
# "network": [1]
# }

class ClusteredArticlesHandler:
    def run(self, labels, terms):
        with open(ARTICLES_PATH, encoding='UTF-8') as f:
            lines = f.readlines()
            for key, value in terms.items():
                os.makedirs(os.path.join("output", "clustering_results", key), exist_ok=True)
                for cluster in value:
                    for index, item in enumerate(labels):
                        if item == cluster:
                            line = lines[index].split(",")
                            filename = line[0].split('/')
                            with open(SAVE_PATH + "/" + key + "/" + filename[len(filename) - 1] + '.txt', 'w') as file:
                                file.write(line[1].replace('"', ""))
