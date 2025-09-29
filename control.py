from re import I
import sys
import pprint
import platform
import csv
import os

from deli_date_folder import DeliDateFolder
import folder_manage
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
        - should_send_coas = [[AHI832, 20250930T], [AHI855, 20250922T],...]
    '''

    def __init__(self)-> None:
        ui: UserInterface = UserInterface()
        self.isTest: bool = ui.get_isTest()
        self.delivery_date: str = ui.get_delivery_date()

        self.folder_manage:FolderManage = FolderManage(self.isTest, 
                                                  self.delivery_date)
        self.deli_date_path: str = self.folder_manage.get_deli_date_path()
        # zip_filesフォルダの中にdeli_date_path(納入日フォルダ)が無ければ作る。
        self.folder_manage.create_deli_date_folder()
        # 納入日のﾌｫﾙﾀﾞの中に送信済フォルダが無ければ、作成する
        self.folder_manage.create_sent_folder()


    def start(self)-> None:
        order_no_should_send = OrderNoShouldSend(self.isTest, self.delivery_date,
                                                 self.deli_date_path
                                                 )

        '''
        should_send_coas = {'AHI832': {'タイ/小糸': [20250930T, 20250921T,...]}, 
                            'AHI855': {'タイ/小糸': [...]} }
        '''
        
        should_send_coas: Dict[str, Dict[str, List[str]]]= (order_no_should_send.
                                                  get_should_send_coas()
                                                 )

        print('should_send_coas..............................')
        print(should_send_coas)

        # ZipedCoaのインスタンス生成 + Coaのインスタンスも
        coas_should_zips: List[CoasShouldZip] = []
        for order_no, dic_dest in should_send_coas.items():
            coas:List[Coa] = []
            for dest, lots in dic_dest.items():
                for lot in lots:
                    coas.append(Coa(order_no, lot))
                coas_should_zips.append(CoasShouldZip(
                                                      order_no, 
                                                      coas, 
                                                      self.deli_date_path, 
                                                      self.isTest, 
                                                      dest
                                                     )
                                       )

        
        # zipファイルを作成
        for coas_should_zip in coas_should_zips:
            coas_should_zip.create_zip()

        # mail送信
        success_send_mails: List[List[str]] = []
        mail_manage: MailManage = MailManage(self.isTest)
        deli_date_folder = DeliDateFolder(mail_manage)
        success_send_mails = deli_date_folder.send_mail()
        
        # deli_date_folderに残ったzipファイルを全て削除する
        self.folder_manage.delete_zip_files()

        print('success_send_mails>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        print(success_send_mails)



        for coas_should_zip in coas_should_zips:
            coas_should_zip.show_coa_lot()
        
        for success_ziped_coa in DeliDateFolder.success_ziped_coas:
            for coa in success_ziped_coa.coas:
                print(coa.lot)

        

