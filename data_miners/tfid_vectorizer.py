import os

from sklearn.feature_extraction.text import TfidfVectorizer
from spiders.cisa_gov_uscert_ics_advisories_content_spider import NAME
from utils.contents_loader import ContentsLoader
from utils.file_saver import FileSaver


# STOP_WORDS = ['I', 'am']
STOP_WORDS = 'english'
TARGET_FILE_NAME = '/content_vectorized.txt'
SOURCE_FILE_NAME = '/content_cleaned.txt'
TARGET_FILE_PATH = 'output/' + NAME + TARGET_FILE_NAME
SOURCE_FILE_PATH = 'output/' + NAME + SOURCE_FILE_NAME


class TfidVectorizer:
    def run(self):
        if os.path.isfile(TARGET_FILE_PATH):
            os.remove(TARGET_FILE_PATH)
        contents_loader = ContentsLoader()
        documents = contents_loader.load_contents(SOURCE_FILE_PATH)
        titles = [document['title'] for document in documents]
        documents = [document['content'].lower() for document in documents]
        vectorizer = TfidfVectorizer(stop_words=STOP_WORDS)
        vectorized_documents = vectorizer.fit_transform(documents)
        vectorized_documents_features = vectorizer.get_feature_names_out()
        vectorized_documents_array = vectorized_documents.toarray()

        file_saver = FileSaver()

        row = 'source URL, '
        for i in range(len(vectorized_documents_features)):
            row += str(vectorized_documents_features[i]) + ', '
        file_saver.save_to_file('output/' + NAME, 'content_vectorized', row)

        for j in range(len(vectorized_documents_array)):
            row = titles[j]+', '
            for i in range(len(vectorized_documents_array[j])):
                row += str(vectorized_documents_array[j][i]) + ', '
            file_saver.save_to_file('output/' + NAME, 'content_vectorized', row)
