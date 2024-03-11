import scrapy

from configurator import SCRAPER_DOWNLOADING_DELAY
from spiders import cisa_gov_uscert_ics_advisories_spider_paths_spider
from utils.contents_saver_pipeline import ContentsSaverPipeline
from utils.file_saver import FileSaver
from utils.paths_loader import PathsLoader

_PIPELINE_PATH = f'{ContentsSaverPipeline.__module__}.{ContentsSaverPipeline.__name__}'
NAME = 'CisaGovUscertIcsAdvisoriesContentSpider'


class CisaGovUscertIcsAdvisoriesContentSpider(scrapy.Spider):
    name = NAME
    start_urls = []
    paths_loader = PathsLoader()
    file_saver = FileSaver()

    custom_settings = {
        'DOWNLOAD_DELAY': SCRAPER_DOWNLOADING_DELAY,
        'ITEM_PIPELINES': {
            _PIPELINE_PATH: 300,
        }
    }

    def __init__(self):
        self.start_urls = self.paths_loader.load_paths(
            'output/' + cisa_gov_uscert_ics_advisories_spider_paths_spider.NAME + '/paths.txt')

    def parse(self, response):
        content = response.xpath('//div[@class="l-content"]//p/text()').extract()
        for paragraph in content:
            yield {'content': paragraph.strip(),
                   'path': response.request.url}
