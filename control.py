import sys
import pprint
import platform
import datetime

from deli_date_folder import DeliDateFolder
from user_interface import UserInterface
from folder_manage import FolderManage
from order_no_should_send import OrderNoShouldSend
from coa import Coa
from coas_should_zip import CoasShouldZip
from mail_manage import MailManage
from typing import List, Dict
from move_coa_to_sousinsumi import MoveCoaToSousinsumi

my_module_path = r'\\192.168.1.247\共有\技術課ﾌｫﾙﾀﾞ\200. effit_data\ﾏｽﾀ\sql_python_module'
if platform.system() == 'Linux':
    my_module_path = r'/mnt/public/技術課ﾌｫﾙﾀﾞ/200. effit_data/ﾏｽﾀ/sql_python_module'
sys.path.append(my_module_path)
from list_contents_of_zip_files import ListContentsOfZipFiles

class Control(object):


    def __init__(self)-> None:
        ui: UserInterface = UserInterface()
        self.__isTest: bool = ui.get_isTest()
        self.__delivery_date: str = ui.get_delivery_date()

        self.__folder_manage:FolderManage = FolderManage(self.__isTest, 
                                                  self.__delivery_date)
        self.__deli_date_path: str = self.__folder_manage.get_deli_date_path()


    def start(self)-> None:
        order_no_should_send = OrderNoShouldSend(self.__isTest, self.__delivery_date,
                                                 self.__deli_date_path
                                                 )

        '''
        should_send_coas = {'AHI832': {'タイ/小糸': [20250930T, 20250921T,...]}, 
                            'AHI855': {'タイ/小糸': [...]} }
        '''
        
        should_send_coas_thisTime: Dict[str, Dict[str, List[str]]]= (
                         order_no_should_send. get_should_send_coas_thisTime()
                                                                         )


        # zip_filesフォルダの中に__deli_date_path(納入日フォルダ)が無ければ作る。
        self.__folder_manage.create_deli_date_folder()
        # 納入日のﾌｫﾙﾀﾞの中に送信済フォルダが無ければ、作成する
        self.__folder_manage.create_sent_folder()
        log_path:str = self.__folder_manage.create_log_file()


        date_deli: str = f'{self.__delivery_date[:4]}/{self.__delivery_date[4:6]}/{self.__delivery_date[6:]}'
        now_time:str = datetime.datetime.now().time().strftime('%H:%M:%S')
        with open(log_path, 'a') as f:
            f.write('納入日  :  ' + date_deli + '\n')
            f.write('時刻    :  ' + now_time + '\n\n')
            if not order_no_should_send.isShouldSendCoas():
                print(f'{date_deli} に送信するCOAはありません')
                f.write(f'{date_deli} に送信するCOAはありません')
                sys.exit()

            if not should_send_coas_thisTime:
                print(f'{date_deli} のCOAは全て送信済みです')
                f.write(f'{date_deli} のCOAは全て送信済みです')
                sys.exit()

        print('\n\n')
        print('zipを作成中>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n')
        





        # ZipedCoaのインスタンス生成 + Coaのインスタンスも
        mail_manage: MailManage = MailManage(self.__isTest)
        coas_should_zips: List[CoasShouldZip] = []
        for order_no, dic_dest in should_send_coas_thisTime.items():
            coas:List[Coa] = []
            for dest, lots in dic_dest.items():
                for lot in lots:
                    coas.append(Coa(order_no, lot))
                coas_should_zips.append(CoasShouldZip(
                                                  order_no, 
                                                  coas, 
                                                  self.__deli_date_path,
                                                  self.__isTest, 
                                                  dest,
                                                  mail_manage
                                                     )
                                       )

        
        # zipファイルを作成
        for coas_should_zip in coas_should_zips:
            coas_should_zip.create_zip()

        # mail送信
        success_send_mails: List[List[str]] = []
        deli_date_folder = DeliDateFolder()
        success_send_mails = deli_date_folder.send_mail()
        
        # deli_date_folderに残ったzipファイルを全て削除する
        self.__folder_manage.delete_zip_files()

        # log
        order_no_should_send.show_should_send_coas(log_path, date_deli)
        order_no_should_send.show_sent_order_nos(log_path)
        order_no_should_send.show_should_send_coas_thisTime(log_path)
        deli_date_folder.show_success_ziped_coas(log_path)
        self.show_success_send_mails(log_path, success_send_mails)
        order_no_should_send.show_target_for_yet(log_path, success_send_mails)

        # ここから送信に成功したzipの中身ファイルを輸出フォルダから送信済み(Robot)フォルダに移動する
        move_coa_to_sousinsumi = MoveCoaToSousinsumi()
        zip_files = ListContentsOfZipFiles() # my_python_module
        # 送信済zipの中身を取り出す
        zip_path = f'{self.__deli_date_path}/送信済'
        all_filenames: List[str] = \
            zip_files.list_contents_of_zip_files(zip_path)
        moved_files: Dict = move_coa_to_sousinsumi.move_files_to_sousinsumi(all_filenames)

        pprint.pprint(moved_files)
        movedfiles: List[str] = moved_files['moved_files']
        notfoundfiles: List[str] = moved_files['not_found_files']
        errors: List[str] = moved_files['errors']

        txt = f'moved_files: {"...".join(movedfiles)} \n' \
        f'not_found_files: {"...".join(notfoundfiles)} \n' \
        f'errors: {"...".join(errors)}'


        print('プログラムは無事終了しました。>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        with open(log_path, 'a') as f:
            f.write(txt)
            f.write('\n\n')
            f.write('プログラムは無事終了しました。>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n')



    def show_success_send_mails(self, log_path: str, success_send_mails: List[List[str]])-> None:
        print(f'(送信に成功した向け先)')
        num: int = 1
        for line in success_send_mails:
            print(f'{num}. {line[0]}, {line[1]}')
            num += 1
        print('\n')

        with open(log_path, 'a') as f:
            f.write(f'(送信に成功した向け先)\n')

            num: int = 1
            for line in success_send_mails:
                f.write(f'{num}. {line[0]}, {line[1]}\n')
                num += 1
            f.write('\n\n')


    def get_deli_date_path(self):
        return self.__deli_date_path
        
    
