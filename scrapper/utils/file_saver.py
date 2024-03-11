import os


class FileSaver:
    def save_to_file(self, dir_to_save, file_name, content):
        if not os.path.exists(dir_to_save):
            os.makedirs(dir_to_save)
        file_object = open(dir_to_save+'/'+file_name+'.txt', 'a+', encoding="UTF-8")
        file_object.write(str(content)+'\n')
        file_object.close()
        print(dir_to_save+' '+file_name+' '+str(content))
