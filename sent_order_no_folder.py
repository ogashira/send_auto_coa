import os
from os.path import isdir
from typing import List
from henkan import Henkan

class SentOrderNoFolder(object):

    def __init__(self, deli_date_path)-> None:
        self.__sent_order_nos: List[str] = []

        sent_folder_path = deli_date_path + '/送信済'
        # フォルダ内のファイルを走査
        if os.path.isdir(deli_date_path):
            for filename in os.listdir(sent_folder_path):
                if filename.lower().endswith(".zip"):
                    filename = filename[:len(filename)-len('.zip')]
                    filename = Henkan.henkan(filename)

                    self.__sent_order_nos.append(filename)
                    '''
                    zip_path = os.path.join(sent_folder_path, filename)
                    # zipファイルを開いて中身を取得
                    with zipfile.ZipFile(zip_path, 'r') as zf:
                        for zip_name in zf.namelist():
                            sent_zips.append(zip_name)
                    '''


    def get_sent_order_nos(self)-> List[str]:
        return self.__sent_order_nos






