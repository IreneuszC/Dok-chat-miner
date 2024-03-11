PAGES_TO_SCRAP = 2
DELIMITER = ','  # ',' / ';'
SCRAPER_DOWNLOADING_DELAY = 2
SENTENCES_TO_CLEAR = ['An official website of the United States government',
                         'CISA is part of the ',
                         'An official website of the United States government ',
                         '"',
                         '\u202f',
                         ' ',
                         'CISA also provides a section for',
                         'This updated advisory is a follow-up to the original advisory titled ICSA',
                         'that was published',
                         'on the ICS webpage on cisa.gov/ICS.',
                         'Successful exploitation of this vulnerability',
                         'Successful exploitation of these vulnerabilities'
                      ]

CLUSTERS_NUMBER = 3
MAX_CLUSTERS_NUMBER_DIVISOR = 10
MIN_CLUSTERS_SAMPLES = 3
QUERY_TERMS = ['ethernet', 'government', 'network']
TARGET_DOCUMENT = 'https://www.cisa.gov/uscert/ics/advisories/icsa-22-298-01'
