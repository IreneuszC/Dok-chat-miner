PAGES_TO_SCRAP = 5
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
                         'on the ICS webpage on',
                         'Successful exploitation of this vulnerability',
                         'Successful exploitation of these vulnerabilities',
                         'we’d welcome your feedback',
                         'CISA recommends users take defensive measures to minimize the risk of exploitation of these vulnerabilities. CISA reminds organizations to perform proper impact analysis and risk assessment prior to deploying defensive measures.',
                         'CISA also provides a section for control systems security recommended practices on the ICS webpage on cisa.gov.',
                         'This product is provided subject to this',
                         'We recently updated our anonymous',
                         'We recently updated our anonymous has been assigned to this vulnerability',
                         'As of January 10 2023 CISA will no longer be updating ICS security advisories for Siemens product vulnerabilities beyond the initial advisory.For the most up-to-date information on vulnerabilities in this advisory please see',
                         'Several CISA products detailing cyber defense best practices are available for reading and download',
                         'CISA reminds organizations to perform proper impact analysis and risk assessment prior to deploying defensive measures'
                      ]

CLUSTERS_NUMBER = 3
MAX_CLUSTERS_NUMBER_DIVISOR = 10
MIN_CLUSTERS_SAMPLES = 3
QUERY_TERMS = ['ethernet', 'government', 'network']
TARGET_DOCUMENT = 'https://www.cisa.gov/uscert/ics/advisories/icsa-22-298-01'
