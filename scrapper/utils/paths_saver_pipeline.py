from itemadapter import ItemAdapter


class PathsSaverPipeline:

    def process_item(self, item, spider):
        item_dict = ItemAdapter(item).asdict()
        href_to_save = item_dict['path']
        if href_to_save is not None and href_to_save.lower().startswith(item_dict['starts_with']
                                                                + item_dict['starts_with_file_filter']):
            path = item_dict['main_path']+href_to_save
            spider.file_saver.save_to_file('output/' + spider.name, 'paths', path)
        return item
