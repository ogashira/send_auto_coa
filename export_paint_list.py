import openpyxl
import datetime
import platform
from typing import List 
from henkan import Henkan

class ExportPaintList(object):

    '''
    輸出塗料連絡表
    [行先, 発送日, 納品日, オーダーﾅﾝﾊﾞｰ, 品名, ロット番号, 入れ目, 数量, 
                                                    成績表記載名, 備考,]
    から、
    指定した納入日の[向け先、注文番号、lot、納期]の2次元ﾘｽﾄを作る
    納期はdatetime(2025, 9, 11)になっているので20250911のstringに変更しておく
    '''


    def __init__(self, delivery_date: str) -> None:
        self.delivery_date: str = delivery_date

        #輸出塗料連絡表のﾃﾞｰﾀを取得
        file_path = './'
        if platform.system() == 'Windows':
            file_path = r'//192.168.1.247/Guest/輸出塗料連絡表.xlsx'
        if platform.system() == 'Linux':
            file_path = r'/mnt/guest/輸出塗料連絡表.xlsx'
        if platform.system() == 'Darwin':
            file_path = r'/Volumes/Guest/輸出塗料連絡表.xlsx'


        wb = openpyxl.load_workbook(file_path, data_only = True)
        ws = wb['輸出塗料連絡表']
        self.all_data = [[cell.value for cell in row] for row in ws]
        # 先頭２行は削除する
        self.all_data = self.all_data[2:]


    def get_export_paints(self)-> List[List[str]]:

        export_paints: List[List[str]] = []
        for row in self.all_data: #self.all_data == 輸出塗料連絡表
            row_list: List[str] = []
            if isinstance(row[2], datetime.datetime):
                str_deli_day = row[2].strftime('%Y%m%d')
                if str_deli_day == self.delivery_date:
                    row_list.append(str(row[0])) # 向け先
                    row_list.append(Henkan.henkan(str(row[3]))) # 注番
                    row_list.append(Henkan.henkan(str(row[5]))) # lot
                    row_list.append(str_deli_day) # 納入日
                    export_paints.append(row_list)
        return export_paints
