import nltk
from nltk.metrics import association

from spiders.cisa_gov_uscert_ics_advisories_content_spider import NAME
from utils.contents_loader import ContentsLoader


class BigRamsMiner:
    def run(self, title):
        contents_loader = ContentsLoader()
        documents = contents_loader.load_contents('output/' + NAME + '/content_cleaned.txt')

        # Liczba kolokacji do znalezienia

        n = 125

        all_tokens = [token for article in documents for token in article['content'].lower().split()
                      if article['title'] == title]

        finder = nltk.BigramCollocationFinder.from_words(all_tokens)
        finder.apply_freq_filter(2)
        finder.apply_word_filter(lambda w: w in nltk.corpus.stopwords.words('english'))
        scorer = association.BigramAssocMeasures.jaccard
        collocations = finder.nbest(scorer, n)

        for collocation in collocations:
            c = 'collocation: ' + ' '.join(collocation)
            print(c)
