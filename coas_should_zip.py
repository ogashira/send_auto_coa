from typing import List, Dict
import zipfile
import platform
import glob
from coa import Coa
from pdf_check import PdfCheck
from deli_date_folder import DeliDateFolder
from mail_manage import MailManage

class CoasShouldZip(object):
    
    def __init__(self, order_no: str, coas: List[Coa], 
                       deli_date_path: str, isTest: bool,
                       destination: str,
                       mail_manage: MailManage)->None:
        self.__order_no: str = order_no
        self.__coas: List[Coa] = coas
        self.__deli_date_path: str = deli_date_path
        self.__isTest: bool = isTest
        self.__destination: str = destination
        self.__mail_manage: MailManage = mail_manage


    def show_orderNo_destination(self, num:int)->None:
        print(f'{num}. {self.__order_no}, {self.__destination}')


    def fwrite_orderNo_destination(self, log_path: str, num:int)->None:
        with open(log_path, 'a') as f:
            f.write(f'{num}. {self.__order_no}, {self.__destination}\n')



    def get_coas(self)-> List[Coa]:
        return self.__coas


    def show_coa_lot(self)-> None:
        print(self.__order_no)
        for coa in self.__coas:
            coa.show_lot()


    def create_zip(self)-> None:
        """
        zipファイルを作成して、成功したファイル名をsuccess_zipに格納する
        注番の中に初物があった時点で、その注番のzipは中止する。
        従って、空のzipもあれば、途中まで入っているzipもある

        pdfファイル名中のlotと注番はexcel VBAの方で、成績書作成時に半角、大文字
        空白削除になるようにプログラムされている。
        """
        
        pcSystem = platform.system()

        if pcSystem == 'Windows':
            pdfPath = r'//192.168.1.247/共有/営業課ﾌｫﾙﾀﾞ/testreport/輸出/'
            splitMoji = '\\'
        elif pcSystem == 'Linux':
            pdfPath = r'/mnt/public/営業課ﾌｫﾙﾀﾞ/testreport/輸出/'
            splitMoji = '/'
        else:
            pdfPath = r'/Volumes/共有/営業課ﾌｫﾙﾀﾞ/testreport/輸出/'
            splitMoji = '/'

        #2022/2/28 zipfile_nameを使ってpdfを検索すると、重複するfileも取れてしま
        #うことがわかった。zip_listを使って、lotと注番で検索し、見つかった時点で
        #breakでfor文を抜ける。
        
        pc = PdfCheck()

        zip_path = r'{}/{}.zip'.format(self.__deli_date_path, self.__order_no) 
        with zipfile.ZipFile(zip_path ,'w') as z:
            find_count: int = 0 # 輸出ﾌｫﾙﾀﾞで見つけたcoaの数
            for coa in self.__coas:
                lot: str = coa.get_lot()
                for f in glob.glob(pdfPath + '*' + lot + '*' 
                                                  + self.__order_no + '*'):
                    tmp = str(f).split(splitMoji)
                    zipName = tmp[-1]
                    # 'S6-V333V55-T-R-EX_25090253T_2025911_商社B/usoffice_F35-1.pdf'
                        
                    tup_error = pc.hatumono_check(str(f))
                    if tup_error[0] == True:
                        print('「初物あるため、zipスキップました」: ' 
                                                              + zipName)
                        with open(self.__deli_date_path + '/log.txt', 'a') as f:
                            f.write('初物中止: ' + zipName + '\n')
                        continue
                    elif tup_error[1] == True:
                        print('「errorがあるため、zipスキップしました」: '
                                                              + zipName)
                        with open(self.__deli_date_path + '/log.txt', 'a') as f:
                            f.write('error中止: ' + zipName + '\n')
                        continue
                    else:
                        z.write(f,zipName)
                        find_count += 1
                        break #lotと注番が一致するpdfが一個見つかったら抜ける。

            # 輸出ﾌｫﾙﾀﾞから見つけたcoaとself.__coasとの数が一致したら、
            # success_ziped_coas(クラス変数)に追加
            if find_count == len(self.__coas):
                DeliDateFolder.append_ziped_coa(self)


    def send_mail(self)-> List[str]:
        success_send_mails: List[str] = [] 
        '''
        success_send_mail = [destination, order_no)
        '''
        success_send_mails = self.__mail_manage.send_mail(self.__destination, self.__order_no, self.__deli_date_path)
        return success_send_mails
