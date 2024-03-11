from math import log

# Wprowadź zapytania do zmiennej corpus
QUERY_TERMS = ['mr.', 'green']


class TfidRawMiner:
    def tf(self, term, doc, normalize=True):
        doc = doc.lower().split()
        if normalize:
            return doc.count(term.lower()) / float(len(doc))
        else:
            return doc.count(term.lower()) / 1.0

    def idf(self, term, corpus):
        num_texts_with_term = len([True for text in corpus if term.lower()
                                   in text.lower().split()])

        # obliczenie wskaźnika tf-idf obejmuje pomnożenie wartości tf mniejszej od 0, więc
        # dla spójnej oceny konieczne jest zwrócenie wartości większej niż 1
        # (pomnożenie dwóch wartości mniejszych niż 1 zwraca mniejszą wartość niż każda z nich)

        try:
            return 1.0 + log(float(len(corpus)) / num_texts_with_term)
        except ZeroDivisionError:
            return 1.0

    def tf_idf(self, term, doc, corpus):
        return self.tf(term, doc) * self.idf(term, corpus)

    def run(self):
        corpus = \
            {'a': 'Mr. Green killed Colonel Mustard in the study with the candlestick. \
        Mr. Green is not a very nice fellow.',
             'b': 'Professor Plum has a green plant in his study.',
             'c': "Miss Scarlett watered Professor Plum's green plant while he was away \
        from his office last week."
             }

        for (k, v) in sorted(corpus.items()):
            print(k, ':', v)
        print()

        # Ocena zapytań poprzez obliczenie skumulowanego wskaźnika tf_idf dla każdego terminu w zapytaniu

        query_scores = {'a': 0, 'b': 0, 'c': 0}
        for term in [t.lower() for t in QUERY_TERMS]:
            for doc in sorted(corpus):
                print('TF({0}): {1}'.format(doc, term), self.tf(term, corpus[doc]))
            print('IDF: {0}'.format(term), self.idf(term, corpus.values()))
            print()

            for doc in sorted(corpus):
                score = self.tf_idf(term, corpus[doc], corpus.values())
                print('TF-IDF({0}): {1}'.format(doc, term), score)
                query_scores[doc] += score
            print()

        print("Ogólny wskaźnik TF-IDF dla zapytania '{0}'".format(' '.join(QUERY_TERMS)))
        for (doc, score) in sorted(query_scores.items()):
            print(doc, score)
