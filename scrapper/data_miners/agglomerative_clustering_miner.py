from matplotlib import pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage
from sklearn.feature_extraction.text import TfidfVectorizer

from data_miners.clusterization_handler import ClusterizationHandler, AGGLOMERATIVE_METHOD
from spiders.cisa_gov_uscert_ics_advisories_content_spider import NAME
from utils.contents_loader import ContentsLoader
from sklearn.cluster import AgglomerativeClustering
import numpy as np


class AgglomerativeClusteringMiner:
    def run(self, clusters_number):
        contents_loader = ContentsLoader()
        documents = contents_loader.load_contents('output/' + NAME + '/content_cleaned.txt')
        documents = [document['content'].lower()
                     for document in documents]
        vectorizer = TfidfVectorizer(stop_words='english')
        X = vectorizer.fit_transform(documents)
        X = np.array(X.toarray())

        methods = ['ward', 'complete', 'average', 'single']
        for clusters_no in range(2, clusters_number):
            for method in methods:
                model = AgglomerativeClustering(
                    n_clusters=clusters_no,
                    affinity="euclidean",
                    linkage=method,

                ).fit(X)
                print('Agglomerative Clustering labels, clusters number: '+str(clusters_no)+', method: '+method+', labels: ' + str(model.labels_))

                # dendrogram(linkage(X, method),
                #            orientation='top',
                #            distance_sort='descending',
                #            show_leaf_counts=True)

                #plt.show()
                clusterization_handler = ClusterizationHandler()
                clusterization_handler.run(AGGLOMERATIVE_METHOD+'/'+method, X, model, 'query_terms', vectorizer, clusters_no)
