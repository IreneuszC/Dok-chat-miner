import nltk

from spiders.cisa_gov_uscert_ics_advisories_content_spider import NAME
from utils.contents_loader import ContentsLoader


class TfidMiner:
    def run(self, query_terms):
        contents_loader = ContentsLoader()
        data = contents_loader.load_contents('output/' + NAME + '/content_cleaned.txt')
        activities = [article['content'].lower().split()
                      for article in data
                        if article['content'] != ""]

        # TextCollection dostarcza abstrakcji tf, idf i tf_idf, zatem
        # nie ma potrzeby, aby je utrzymywać (wyliczać) samodzielnie

        tc = nltk.TextCollection(activities)

        relevant_activities = []

        for idx in range(len(activities)):
            score = 0
            for term in [t.lower() for t in query_terms]:
                score += tc.tf_idf(term, activities[idx])
            if score > 0:
                relevant_activities.append({'score': score, 'title': data[idx]['title']})

        # Posortuj według oceny i wyświetl wyniki

        relevant_activities = sorted(relevant_activities,
                                     key=lambda p: p['score'], reverse=True)
        for activity in relevant_activities:
            print('Tytuł: {0}'.format(activity['title']))
            print('Ocena: {0}'.format(activity['score']))
            print()
