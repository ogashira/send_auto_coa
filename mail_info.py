import openpyxl
import platform
from typing import List 

class MailInfo(object):

    def __init__(self, isTest:bool)-> None:

        self.isTest: bool = isTest

        #ﾒｰﾙ送信先情報のﾃﾞｰﾀを取得
        if self.isTest:
            if platform.system() == 'Windows':
                bookPath = r'//192.168.1.247/共有/技術課ﾌｫﾙﾀﾞ/200. effit_data/' \
                                     r'ﾏｽﾀ/coaﾒｰﾙ送信関連/test_ﾒｰﾙ送信先情報.xlsx'
            elif platform.system() == 'Linux':
                bookPath = r'/mnt/public/技術課ﾌｫﾙﾀﾞ/200. effit_data/' \
                                     r'ﾏｽﾀ/coaﾒｰﾙ送信関連/test_ﾒｰﾙ送信先情報.xlsx'
            else:
                bookPath = r'/Volumes/共有/技術課ﾌｫﾙﾀﾞ/200. effit_data/' \
                                     r'ﾏｽﾀ/coaﾒｰﾙ送信関連/test_ﾒｰﾙ送信先情報.xlsx'
        else:
            if platform.system() == 'Windows':
                bookPath = r'//192.168.1.247/共有/技術課ﾌｫﾙﾀﾞ/200. effit_data/' \
                                     r'ﾏｽﾀ/coaﾒｰﾙ送信関連/ﾒｰﾙ送信先情報.xlsx'
            elif platform.system() == 'Linux':
                bookPath = r'/mnt/public/技術課ﾌｫﾙﾀﾞ/200. effit_data/' \
                                     r'ﾏｽﾀ/coaﾒｰﾙ送信関連/ﾒｰﾙ送信先情報.xlsx'
            else:
                bookPath = r'/Volumes/共有/技術課ﾌｫﾙﾀﾞ/200. effit_data/' \
                                     r'ﾏｽﾀ/coaﾒｰﾙ送信関連/ﾒｰﾙ送信先情報.xlsx'


        wb = openpyxl.load_workbook(bookPath, data_only = True)
        ws = wb['ﾒｰﾙ送信先情報']
        self.mail_infos:List[List[str]] = [[str(cell.value) for cell in row] for row in ws]
        '''
        [ [ '長瀬', '広州/スタンレー', '長瀬産業株式会社', '瀬川様', address],
        ]
        '''

        #向け先のﾘｽﾄを作成する
        self.destinations: List[str] = []
        for mail_info in self.mail_infos:
            self.destinations.append(mail_info[1])
        '''
        ['北米/スタンレー', '広州/スタンレー', ........]
        '''

    def get_mail_infos(self)-> List[List[str]]:
        return self.mail_infos

    def get_destinations(self)-> List[str]:
        return self.destinations
