#! python
# -*- coding:utf-8 -*-

import os
import shutil
import platform
import smtplib
import yaml

from typing import List
from email.mime.text import MIMEText
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.base import MIMEBase
from email import encoders
from mail_info import MailInfo



class MailManage(object):

    def __init__(self, isTest)-> None:

        self.__isTest: bool = isTest

        yaml_path = './'
        if platform.system() == 'Windows':
            yaml_path = r'//192.168.1.247/共有/技術課ﾌｫﾙﾀﾞ/200. effit_data/ﾏｽﾀ/coaﾒｰﾙ送信関連/mail_info.yaml'
        if platform.system() == 'Linux':
            yaml_path = r'/mnt/public/技術課ﾌｫﾙﾀﾞ/200. effit_data/ﾏｽﾀ/coaﾒｰﾙ送信関連/mail_info.yaml'
        if platform.system() == 'Darwin':
            yaml_path = r'/Volumes/共有/技術課ﾌｫﾙﾀﾞ/200. effit_data/ﾏｽﾀ/coaﾒｰﾙ送信関連/mail_info.yaml'

        with open(yaml_path, 'r') as file:
            self.__yaml_data = yaml.safe_load(file)

        mail_info = MailInfo(isTest)
        self.__mail_infos: List[List[str]] = mail_info.get_mail_infos()
        '''
        self.__mail_infos 
        [ [ '長瀬', '広州/スタンレー', '長瀬産業株式会社', '瀬川様', address],
        ]
        '''


    def send_mail(self, destination: str, order_no: str, deli_date_path: str )-> List[str]:

        def get_nouki() -> str:
            list_path: List[str] = deli_date_path.split('/')
            nouki_num = list_path[-1]
            if '_test' in nouki_num:
                nouki_num = nouki_num[:len(nouki_num) - len('_test')]

            nouki: str = nouki_num[:4] + '/' + nouki_num[4:6] + '/' + nouki_num[6:]

            return nouki


        def move_successSendZipFiles(zipPath, dst_folder):
            dst_path = os.path.join(dst_folder, os.path.basename(zipPath))
            shutil.move(zipPath, dst_path)


        success_send_mail: List[str] = []
        officeName = ""
        tantou = ""
        mailAddress = ""
        for mail_info in self.__mail_infos:
            officeName = ""
            if destination == mail_info[1]:
                officeName = mail_info[2]
                tantou = mail_info[3]
                mailAddress = mail_info[4]
                break

        charset = 'iso-2022-jp'

        #smtp_host = 'smtp.toyo-jupiter.co.jp'
        smtp_host = self.__yaml_data['eigyou']['smtp_host']
        smtp_port= self.__yaml_data['eigyou']['smtp_port']
        username = self.__yaml_data['eigyou']['username']
        password = self.__yaml_data['eigyou']['password']
        from_address = self.__yaml_data['eigyou']['from_address']
        to_address = mailAddress
        cc = self.__yaml_data['eigyou']['cc']
        if self.__isTest:
            cc = ''
        
        # to_address = [to_address] + cc
        nouki:str = get_nouki()

        body = MIMEText(
                '{} \n'
                '{} \n'
                '\n\n' 
                'いつも大変お世話になっております \n'
                '下記の成績書を送付いたしました。 \n\n'
                '納期： {} \n'
                '注文番号： {} \n\n'
                'よろしくお願い申し上げます。\n\n\n'
                '東洋工業塗料株式会社 \n'
                '松戸\n\n'.format(
                    officeName, tantou, nouki, order_no), 
                 'plain', charset)

        # body['subject'] = Header('検査成績書送付の件',  charset)

        msg = MIMEMultipart()

        msg['Subject'] = order_no + ' 成績書'
        msg['From'] = from_address
        msg['To'] = to_address
        msg['Cc'] = cc
        msg.attach(body)


        zipPath = r'{}/{}.zip'.format(deli_date_path, order_no)  
            


        attach = MIMEBase('application', 'zip')
        try:
            with open(zipPath, 'br') as f:
                attach.set_payload(f.read())
                encoders.encode_base64(attach)
                attach.add_header("Content-Disposition", "attachement", 
                                                  filename = order_no + '.zip')
                msg.attach(attach)

            smtp = smtplib.SMTP(smtp_host, smtp_port)
            smtp.login(username, password)
            smtp.send_message(msg)
            success_send_mail.append(order_no)
            success_send_mail.append(destination)
            smtp.quit
            move_successSendZipFiles(zipPath,  deli_date_path + '/送信済')
        except Exception:
            print('mail送信失敗')


        return success_send_mail



    

    def get_finally_fail_mail(self, zipfile_info, success_send_mail):
        '''
        最終的に送信できなかった向け先を求める
        zipで失敗したり、送信でｴﾗｰになったりしたもの
        zipfile_infoの中身を１つずつ回して、success_send_mail
        に存在していなければ、finally_fail_mailにappendする
        '''

        finally_fail_mail = []
        for info in zipfile_info:
            if info not in success_send_mail:
                finally_fail_mail.append(info)
        return finally_fail_mail


