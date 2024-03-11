import nltk.cluster

from spiders.cisa_gov_uscert_ics_advisories_content_spider import NAME
from utils.contents_loader import ContentsLoader


class CosineSimilarityMiner:
    def run(self):
        contents_loader = ContentsLoader()
        data = contents_loader.load_contents('output/' + NAME + '/content_cleaned.txt')

        all_articles = [(i['title'] + " " + i['content']).lower().split() for i in data]

        # Dostarczenie abstrakcji tf, idf i tf_idf do oceny

        tc = nltk.TextCollection(all_articles)

        # Obliczenie macierzy hasło-dokument w taki sposób, że td_matrix [doc_title] [term]
        # zwraca ocenę tf-idf dla hasła w dokumencie

        td_matrix = {}
        for idx in range(len(all_articles)):
            post = all_articles[idx]
            fdist = nltk.FreqDist(post)

            doc_title = data[idx]['title'].replace('\n', '')
            td_matrix[doc_title] = {}

            for term in fdist.keys():
                td_matrix[doc_title][term] = tc.tf_idf(term, post)

        # Zbudowanie wektorów w taki sposób, aby wyniki haseł były na tych samych pozycjach
        distances = {}
        for title1 in td_matrix.keys():

            distances[title1] = {}
            (min_dist, most_similar) = (1.0, ('', ''))

            for title2 in td_matrix.keys():

                # Uważaj, aby nie zmodyfikować wejściowych struktur danych
                # Jesteśmy w pętli i potrzebujemy oryginałów wiele razy.

                terms1 = td_matrix[title1].copy()
                terms2 = td_matrix[title2].copy()

                # Wypełnij „luki” w każdej mapie tak, aby można było obliczać wektory o tej samej długości
                for term1 in terms1:
                    if term1 not in terms2:
                        terms2[term1] = 0

                for term2 in terms2:
                    if term2 not in terms1:
                        terms1[term2] = 0

                # Utworzenie wektorów z map haseł.
                v1 = [score for (term, score) in sorted(terms1.items())]
                v2 = [score for (term, score) in sorted(terms2.items())]

                # Obliczenie podobieństwa pomiędzy dokumentami
                distances[title1][title2] = nltk.cluster.util.cosine_distance(v1, v2)

                if title1 == title2:
                    #print distances[title1][title2]
                    continue

                if distances[title1][title2] < min_dist:
                    (min_dist, most_similar) = (distances[title1][title2], title2)

            print(u'Najbardziej podobny (ocena: {})\n{}\n{}\n'.format(1-min_dist, title1,
                                                               most_similar))
            #break;
