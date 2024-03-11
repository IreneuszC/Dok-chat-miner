import os
import shutil
import scrapy
from configurator import PAGES_TO_SCRAP
from utils.file_saver import FileSaver
from utils.paths_saver_pipeline import PathsSaverPipeline

_PIPELINE_PATH = f'{PathsSaverPipeline.__module__}.{PathsSaverPipeline.__name__}'
NAME = 'CisaGovUscertIcsAdvisoriesPathsSpider'
MAIN_PATH = "https://www.cisa.gov"
ARTICLES_PATH = 'https://www.cisa.gov/news-events/cybersecurity-advisories?f%5B0%5D=advisory_type%3A95'
STARTS_WITH = '/news-events/ics-advisories'
STARTS_WITH_FILES_FILTER = '/ic'


class CisaGovUscertIcsAdvisoriesPathsSpider(scrapy.Spider):
    name = NAME
    file_saver = FileSaver()

    custom_settings = {
        'ITEM_PIPELINES': {
            _PIPELINE_PATH: 300,
        }
    }

    def start_requests(self):
        for page in range(0, PAGES_TO_SCRAP):
            yield scrapy.Request(f'https://www.cisa.gov/news-events/cybersecurity-advisories?f%5B0%5D=advisory_type%3A95&page={page}')


    def parse(self, response):
        if os.path.exists('output/' + NAME):
            shutil.rmtree('output/' + NAME)

        for path in response.xpath('//a'):
            pathExtracted = path.xpath('@href').get()
            if pathExtracted.startswith(STARTS_WITH):
                print(pathExtracted)
            yield {'path': path.xpath('./@href').get(),
                   'main_path': MAIN_PATH,
                   'starts_with': STARTS_WITH,
                   'starts_with_file_filter': STARTS_WITH_FILES_FILTER}
