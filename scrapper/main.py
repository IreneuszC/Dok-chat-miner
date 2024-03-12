import nltk
from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from nltk.corpus import stopwords

from configurator import CLUSTERS_NUMBER, QUERY_TERMS, TARGET_DOCUMENT
from data_miners.agglomerative_clustering_miner import AgglomerativeClusteringMiner
from data_miners.bigrams_miner import BigRamsMiner
from data_miners.cosine_similarity_miner import CosineSimilarityMiner
from data_miners.dbscan_miner import DbScanMiner
from data_miners.kmeans_miner import KmeansMiner
from data_miners.tfid_miner import TfidMiner
from data_miners.tfid_raw_miner import TfidRawMiner
from data_miners.tfid_vectorizer import TfidVectorizer
from spiders import cisa_gov_uscert_ics_advisories_spider_paths_spider, cisa_gov_uscert_ics_advisories_content_spider
from spiders.cisa_gov_uscert_ics_advisories_content_spider import CisaGovUscertIcsAdvisoriesContentSpider
from spiders.cisa_gov_uscert_ics_advisories_spider_paths_spider import CisaGovUscertIcsAdvisoriesPathsSpider
from utils.contents_cleaner import ContentsCleaner


@defer.inlineCallbacks
def crawl():
    yield runner.crawl(CisaGovUscertIcsAdvisoriesPathsSpider)
    yield runner.crawl(CisaGovUscertIcsAdvisoriesContentSpider)
    reactor.stop()


# To build env use this command in terminal: conda env create -f environment.yml
# To update use: conda env update --file environment.yml --prune
# Press the green button in the gutter to run the script.

if __name__ == '__main__':

    query_terms = QUERY_TERMS
    clusters_number = CLUSTERS_NUMBER

    if 1:
        configure_logging()
        runner = CrawlerRunner()
        crawl()
        reactor.run()

    if 1:
        contents_cleaner = ContentsCleaner()
        contents_cleaner.clear_contents(cisa_gov_uscert_ics_advisories_content_spider.NAME,
                                        'output/' + cisa_gov_uscert_ics_advisories_content_spider.NAME + '/content.txt')

    if 0:
        nltk.download('stopwords')

    if 0:
        tfid_vectorizer = TfidVectorizer()
        tfid_vectorizer.run()

    if 1:
        kmeans_miner = KmeansMiner()
        clusters_number = kmeans_miner.run(query_terms, clusters_number)

    if 1:
        dbscan_miner = DbScanMiner()
        dbscan_miner.run(query_terms)

    if 1:
        agglomerative_clustering_miner = AgglomerativeClusteringMiner()
        agglomerative_clustering_miner.run(clusters_number, query_terms)

    if 0:
        tfid_miner = TfidMiner()
        tfid_miner.run(query_terms)

    if 0:
        cosine_similarity_miner = CosineSimilarityMiner()
        cosine_similarity_miner.run()

    if 0:
        big_rams_miner = BigRamsMiner()
        big_rams_miner.run(TARGET_DOCUMENT)
