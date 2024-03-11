from sklearn.metrics import silhouette_score

import configurator
from utils.file_saver import FileSaver
from data_miners.clustered_articles_handler import ClusteredArticlesHandler

KMEANS_METHOD = 'kmeans'
DBSCAN_METHOD = 'dbscan'
AGGLOMERATIVE_METHOD = 'SilhouetteResults'


class ClusterizationHandler:
    def run(self, method_name, X, model, query_terms, vectorizer, clusters_number):

        print('method: ' + method_name)

        file_saver = FileSaver()
        if clusters_number > 1:
            score = silhouette_score(X, model.labels_)
            print('silhouette_score: ' + str(score))
            file_saver.save_to_file('output/' + 'clustering_results', 'silhouette',
                                    method_name + configurator.DELIMITER
                                    + str(clusters_number) + configurator.DELIMITER + str(score))

        print('labels: '+ str(model.labels_))

        if method_name == KMEANS_METHOD:
            print('Top terms per cluster: ')
            order_centroids = model.cluster_centers_.argsort()[:, ::-1]
            terms = vectorizer.get_feature_names_out()

            for i in range(clusters_number):
                print('Cluster %d:' % i),
                for ind in order_centroids[i, :10]:
                    print(' %s' % terms[ind]),
                print()

            print('\n')
            if query_terms is not None:
                termsDict = {}
                print('Prediction: ')
                for query_term in query_terms:
                    Y = vectorizer.transform([query_term])
                    prediction = model.predict(Y)
                    print(query_term + ':' + str(prediction))
                    termsDict[query_term] = prediction

                clusteredArticlesHandlers = ClusteredArticlesHandler()
                clusteredArticlesHandlers.run(model.labels_, termsDict)
