from re import I
import sys
import pprint
import platform
import csv
import os
import datetime

from deli_date_folder import DeliDateFolder
from user_interface import UserInterface
from folder_manage import FolderManage
from order_no_should_send import OrderNoShouldSend
from coa import Coa
from coas_should_zip import CoasShouldZip
from mail_manage import MailManage
'''
from get_exists_coa import GetExistsCoa
from shipment_info import ShipmentInfo
from coa_preparation import CoaPreparation
from zip_check import ZipCheck
'''
from typing import List, Dict



class Control(object):

    '''
    delivery_date : inputした20220930
    DestinationShouldSendでcoaを送らなければならない向け先を求める
        - FolderManageで必要なフォルダを作っておく
        - ExportPaintList(輸出塗料連絡表)で納期日のリストを求め
        - MailInfo(メール送信情報)でリストを絞り込む
        - 更にSentOrderNo(送信済み)から未送信の注番should_send_order_nosを絞る
    '''

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

        
        print('success_send_mails>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        print(success_send_mails)



        for coas_should_zip in coas_should_zips:
            coas_should_zip.show_coa_lot()
        

        for success_ziped_coa in DeliDateFolder.success_ziped_coas: #クラス変数
            for coa in success_ziped_coa.get_coas(): #get_coas()はCoaのリスト
                print(coa.get_lot())

        
        '''
        {}に送信が必要なCOA
        zipに成功したCOA
        zipで失敗したCOA
        {}に送信が必要な向け先
        zipに成功して送信をする向け先
        送信に成功した向け先
        最終的に送信できなかった向け先
        プログラムは無事終了しました。
        '''
        '''
        {}に送信が必要なCOA            OrderNoShouldSend.export_paints
        {}に送信が必要な向け先         should_send_coas       
        すでに送信済みの向け先         OrderNoShouldSend.show_sent_order_nos
        zipで失敗したCOA
        送信に成功した向け先           this.success_send_mails
        まだ送信出来ていない向け先
        プログラムは無事終了しました。
        '''
