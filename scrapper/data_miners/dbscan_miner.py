from kneed import KneeLocator
from matplotlib import pyplot as plt
from sklearn.cluster import DBSCAN
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors

from configurator import MIN_CLUSTERS_SAMPLES
from data_miners.clusterization_handler import ClusterizationHandler, DBSCAN_METHOD
from spiders.cisa_gov_uscert_ics_advisories_content_spider import NAME
from utils.contents_loader import ContentsLoader


class DbScanMiner:
    def run(self, query_terms):
        print('\n')
        contents_loader = ContentsLoader()
        documents = contents_loader.load_contents('output/' + NAME + '/content_cleaned.txt')
        documents = [document['content'].lower()
                     for document in documents]
        vectorizer = TfidfVectorizer(stop_words='english')
        X = vectorizer.fit_transform(documents)
        X = np.array(X.toarray())

        rows, cols = X.shape
        print('Vectorized columns: '+str(cols))
        print('Vectorized rows: ' + str(rows))

        len_documents = cols

        if MIN_CLUSTERS_SAMPLES is not None:
            min_samples = MIN_CLUSTERS_SAMPLES
        else:
            min_samples = 2 * len_documents

        neigh = NearestNeighbors(n_neighbors=min_samples)
        nbrs = neigh.fit(X)
        distances, indices = nbrs.kneighbors(X)
        distances = np.sort(distances, axis=0)
        distances = distances[:, 1]

        plt.style.use("fivethirtyeight")
        plt.plot(distances)
        plt.xticks(range(1, rows))
        plt.xlabel("Number of Clusters")
        plt.ylabel("SSE")
        #plt.show()
        kl = KneeLocator(
            range(1, len(distances)+1), distances, curve="convex", direction="decreasing"
        )
        print('DBSCAN eps ' + str(kl.elbow))
        eps = kl.elbow

        model = DBSCAN(eps=eps, min_samples=min_samples).fit(X)

        labels = model.labels_
        clusters_number=len(set(labels))-(1 if -1 in labels else 0)
        print('Estimated no. of clusters DBSCAN: %d' % clusters_number)

        clusterization_handler = ClusterizationHandler()
        # clusterization_handler.run(DBSCAN_METHOD+"/eps:"+str(eps)+"min_samples:"+str(min_samples), X, model, query_terms, vectorizer, clusters_number)
        clusterization_handler.run(DBSCAN_METHOD, X, model, query_terms, vectorizer, clusters_number, "eps=" + str(eps) + ";min_samples=" + str(min_samples))
