import os
import platform
import zipfile

class FolderManage(object):

    def __init__ (self, isTest: bool, delivery_date: str)->None:
        self.isTest:bool = isTest
        self.deli_date: str = delivery_date
        self.deli_date_path = './'

        if platform.system() == 'Windows':
            self.deli_date_path =  (r'//192.168.1.247/共有/営業課ﾌｫﾙﾀﾞ/testreport/zip_files/' 
                                                                 + self.deli_date)
        if platform.system() == 'Linux':
            self.deli_date_path =  (r'/mnt/public/営業課ﾌｫﾙﾀﾞ/testreport/zip_files/' 
                                                                 + self.deli_date)
        if platform.system() == 'Darwin':
            self.deli_date_path =  (r'/Volumes/共有/営業課ﾌｫﾙﾀﾞ/testreport/zip_files/' 
                                                                 + self.deli_date)

        if self.isTest:
            self.deli_date_path += '_test'


    def get_deli_date_path(self)-> str:
        return self.deli_date_path


    def create_deli_date_folder(self) -> None:
        '''
        zip_filesﾌｫﾙﾀﾞの中に、納入日のﾌｫﾙﾀﾞが無ければ、作成する
        '''

        if not os.path.isdir(self.deli_date_path):
            os.mkdir(self.deli_date_path)


    def create_sent_folder(self) -> None:
        '''
        納入日のﾌｫﾙﾀﾞの中に送信済フォルダが無ければ、作成する
        '''
        sent_folder_path = self.deli_date_path + '/送信済'

        if not os.path.isdir(sent_folder_path):
            os.mkdir(sent_folder_path)


    def delete_zip_files(self) -> None:
        # deli_date_folderに残ったzipファイルを全て削除する
        for filename in os.listdir(self.deli_date_path):
            if filename.lower().endswith(".zip"):
                file_path = os.path.join(self.deli_date_path, filename)
                if os.path.isfile(file_path):
                    os.remove(file_path)
