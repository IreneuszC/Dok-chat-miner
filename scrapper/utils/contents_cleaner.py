import os

import pandas as pd

import configurator
from spiders.cisa_gov_uscert_ics_advisories_content_spider import NAME
from utils.file_saver import FileSaver


class ContentsCleaner:
    def clear_contents(self, spider_name, file_path):
        df = pd.read_csv(file_path, encoding='UTF-8')
        sorted_df = df.sort_values(df.columns[0])
        sorted_df.to_csv('output/' + NAME + '/content_sorted.txt', index=False, encoding='UTF-8')

        if os.path.exists('output/' + NAME + '/content_cleaned.txt'):
            os.remove('output/' + NAME + '/content_cleaned.txt')
            #, encoding='cp1252'
        with open('output/' + NAME + '/content_sorted.txt', encoding='UTF-8') as file:
            temporary_path_content = ''
            last_title = ''
            is_new_content_saved = False
            for line in file:
                line_text = line.rstrip()
                title = line_text.split(",")[0]
                content = line_text.split(",")[-1]
                for sentence in configurator.SENTENCES_TO_CLEAR:
                    content = content.replace(sentence, '')

                if title != last_title and last_title != '':
                    file_saver = FileSaver()
                    temporary_path_content = temporary_path_content.split('For any questions related to this report')[0]
                    file_saver.save_to_file('output/' + spider_name, 'content_cleaned',
                                            last_title + configurator.DELIMITER
                                            + '"' + temporary_path_content + '"')
                    last_title = title
                    temporary_path_content = content
                    is_new_content_saved = True

                elif last_title == '':
                    temporary_path_content = content
                    last_title = title
                    is_new_content_saved = False
                else:
                    temporary_path_content = temporary_path_content + ' ' + content
                    is_new_content_saved = False

            if not is_new_content_saved:
                file_saver = FileSaver()
                temporary_path_content = temporary_path_content.split('For any questions related to this report')[0]
                file_saver.save_to_file('output/' + spider_name, 'content_cleaned',
                                        last_title + configurator.DELIMITER
                                        + '"' + temporary_path_content + '"')
