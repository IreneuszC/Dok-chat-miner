from itemadapter import ItemAdapter
import configurator


class ContentsSaverPipeline:

    def process_item(self, item, spider):
        item_dict = ItemAdapter(item).asdict()
        content_to_save = item_dict['content'].replace(configurator.DELIMITER, '')
        content_to_save = content_to_save.strip()
        if content_to_save is not None:
            spider.file_saver.save_to_file('output/' + spider.name, 'content',
                                           item_dict['path'] + configurator.DELIMITER
                                           + '"' + content_to_save + '"')
        return item
