from datetime import datetime

from kneed import KneeLocator
from matplotlib import pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

from configurator import MAX_CLUSTERS_NUMBER_DIVISOR
from data_miners.clusterization_handler import ClusterizationHandler, KMEANS_METHOD
from spiders.cisa_gov_uscert_ics_advisories_content_spider import NAME
from utils.contents_loader import ContentsLoader


class KmeansMiner:
    def run(self, query_terms, clusters_number):
        print('\n')
        contents_loader = ContentsLoader()
        documents = contents_loader.load_contents('output/' + NAME + '/content_cleaned.txt')
        documents = [document['content'].lower()
                     for document in documents]
        vectorizer = TfidfVectorizer(stop_words='english')
        X = vectorizer.fit_transform(documents)

        max_iter = 100
        n_init = 1

        if clusters_number is None:
            sse = []
            elbow_range = round(len(documents)/MAX_CLUSTERS_NUMBER_DIVISOR)
            for k in range(1, elbow_range):
                print('processing '+str(k)+'/'+str(elbow_range))
                print('started kmeans part 1 at '+str(datetime.now()))
                kmeans = KMeans(n_clusters=k, init='k-means++', max_iter=max_iter, n_init=n_init)
                kmeans.fit(X)
                print('finished kmeans part 1 at '+str(datetime.now()))
                sse.append(kmeans.inertia_)
            # plt.style.use("fivethirtyeight")
            # plt.plot(range(1, elbow_range), sse)
            # plt.xticks(range(1, elbow_range))
            # plt.xlabel("Number of Clusters")
            # plt.ylabel("SSE")
            # plt.show()
            print('Running Knee locator...')
            print('started kmeans part 2 at '+str(datetime.now()))

            kl = KneeLocator(
                range(1, elbow_range), sse, curve="convex", direction="decreasing"
            )
            print('finished kmeans part 2 at '+str(datetime.now()))

            true_k = kl.elbow
        else:
            true_k = clusters_number

        print('Kmeans clusters: ' + str(true_k))
        model = KMeans(n_clusters=true_k, init='k-means++', max_iter=max_iter, n_init=n_init)
        model.fit(X)

        clusterization_handler = ClusterizationHandler()
        clusterization_handler.run(KMEANS_METHOD, X, model, query_terms, vectorizer, true_k)
        return true_k
