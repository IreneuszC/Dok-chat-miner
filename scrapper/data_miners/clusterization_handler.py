import os
import shutil

from sklearn.metrics import silhouette_score

import configurator
from sklearn.metrics.pairwise import cosine_similarity, pairwise_distances
from utils.file_saver import FileSaver
from data_miners.clustered_articles_handler import ClusteredArticlesHandler

KMEANS_METHOD = 'kmeans'
DBSCAN_METHOD = 'dbscan'
AGGLOMERATIVE_METHOD = 'agglomerative'

class ClusterizationHandler:
    def run(self, method_name, X, model, query_terms, vectorizer, clusters_number, additional_method_parameters=''):
        labels = model.labels_
        method_name_with_parameters = method_name + '-' + additional_method_parameters if additional_method_parameters else method_name

        clustered_articles_handler = ClusteredArticlesHandler()

        print('method: ' + method_name_with_parameters)
        print("labels", labels)

        self.calculate_and_save_silhouette_score(X, labels, clusters_number, method_name_with_parameters)

        if method_name == AGGLOMERATIVE_METHOD:
            self.handle_agglomerative_method(X, vectorizer, labels, query_terms, clustered_articles_handler, method_name_with_parameters)

        if method_name == DBSCAN_METHOD:
            self.handle_dbscan_method(X, model, vectorizer, labels, query_terms, clustered_articles_handler, method_name_with_parameters)

        if method_name == KMEANS_METHOD:
            self.handle_kmeans_method(X, model, clusters_number, vectorizer, labels, query_terms, clustered_articles_handler, method_name_with_parameters)

        print('---------------------------------------------------------------------------------')

    def get_cluster_keywords(self, X, vectorizer, top_n=10):
        term_counts = [sum(row) for row in zip(*X)]
        term_indices = sorted(range(len(term_counts)), key=lambda i: term_counts[i], reverse=True)[:top_n]
        terms = vectorizer.get_feature_names_out()
        return [terms[i] for i in term_indices]

    def calculate_and_save_silhouette_score(self, X, labels, clusters_number, method_name):
        file_saver = FileSaver()
        if clusters_number > 1:
            score = silhouette_score(X, labels)
            print('silhouette_score: ' + str(score))
            file_saver.save_to_file('output/' + 'clustering_results', 'silhouette',
                                    method_name + configurator.DELIMITER
                                    + str(clusters_number) + configurator.DELIMITER + str(score))

    def delete_dir(self, dirname):
        results_path = 'output/clustering_results/' + dirname
        if os.path.exists(results_path):
            shutil.rmtree(results_path)

    def handle_kmeans_method(self, X, model, clusters_number, vectorizer, labels, query_terms, clustered_articles_handler, method_name_with_parameters):
        self.delete_dir(method_name_with_parameters)
        print('Top terms per cluster:')
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

            clustered_articles_handler.run(labels, termsDict, method_name_with_parameters)

    def handle_agglomerative_method(self, X, vectorizer, labels, query_terms, clustered_articles_handler, method_name_with_parameters):
        self.delete_dir(method_name_with_parameters)
        print('Top terms per cluster:')
        unique_labels = set(labels)
        for label in unique_labels:
            print("\nCluster %d:" % label)
            cluster_indices = [i for i in range(len(labels)) if labels[i] == label]
            cluster_X = [X[i] for i in cluster_indices]

            # Znajdź słowa kluczowe dla klastra
            terms = vectorizer.get_feature_names_out()
            cluster_keywords = self.get_cluster_keywords(cluster_X, vectorizer, top_n=10)
            for cluster_word in cluster_keywords:
                print(cluster_word)

        # Utwórz centra klastrów jako średnią punktów w klastrze
        centers = []
        for label in unique_labels:
            cluster_indices = [i for i in range(len(labels)) if labels[i] == label]
            cluster_X = [X[i] for i in cluster_indices]
            center = [sum(x) / len(x) for x in zip(*cluster_X)]
            centers.append(center)

        # Oblicz odległość punktu Y od centrów klastrów i przypisz do najbliższego klastra
        if query_terms is not None:
            termsDict = {}
            print('\nPrediction:')
            for query_term in query_terms:
                if query_term in vectorizer.vocabulary_:  # Sprawdzamy, czy słowo kluczowe istnieje w słowniku
                    query_vector = [0] * len(
                        vectorizer.vocabulary_)  # Tworzymy wektor zer o długości równej liczbie cech w danych treningowych
                    query_vector[vectorizer.vocabulary_[
                        query_term]] = 1  # Ustawiamy indeks odpowiadający słowu kluczowemu na 1

                    min_distance = float('inf')
                    nearest_cluster_label = None
                    for center_index, center_point in enumerate(centers):
                        distance = sum((a - b) ** 2 for a, b in zip(query_vector, center_point)) ** 0.5
                        if distance < min_distance:
                            min_distance = distance
                            nearest_cluster_label = list(unique_labels)[center_index]

                    termsDict[query_term] = [nearest_cluster_label]
                    print(query_term + ':' + str(nearest_cluster_label))
                else:
                    print("Keyword '{}' is not present in dictionary.".format(query_term))

            clustered_articles_handler.run(labels, termsDict, method_name_with_parameters)

    def handle_dbscan_method(self, X, model, vectorizer, labels, query_terms, clustered_articles_handler, method_name_with_parameters):
        self.delete_dir(method_name_with_parameters)
        print('Top terms per cluster:')
        core_samples = model.core_sample_indices_
        unique_labels = set(labels)
        for label in unique_labels:
            if label != -1:
                print("\nCluster %d:" % label)
                cluster_indices = [i for i in range(len(labels)) if labels[i] == label]
                cluster_X = [X[i] for i in cluster_indices]
                cluster_keywords = self.get_cluster_keywords(cluster_X, vectorizer, top_n=10)
                for cluster_word in cluster_keywords:
                    print(cluster_word)

        if query_terms is not None:
            termsDict = {}
            print('\n\nPrediction:')
            for query_term in query_terms:
                Y = vectorizer.transform([query_term])
                min_distance = float('inf')
                nearest_cluster_label = None
                for center_index, center_point in enumerate(model.components_):
                    distance = pairwise_distances(Y, [center_point], metric='euclidean')[0][0]
                    if distance < min_distance:
                        min_distance = distance
                        nearest_cluster_label = labels[core_samples[center_index]]

                print(query_term + ':' + str([nearest_cluster_label]))

                termsDict[query_term] = [nearest_cluster_label]

            clustered_articles_handler.run(labels, termsDict, method_name_with_parameters)