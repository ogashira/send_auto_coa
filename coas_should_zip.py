from typing import List, Dict
import zipfile
import platform
import glob
from coa import Coa
from pdf_check import PdfCheck
from deli_date_folder import DeliDateFolder

class CoasShouldZip(object):
    
    def __init__(self, order_no: str, coas: List[Coa], 
                       deli_date_path: str, isTest: bool,
                       destination: str)->None:
        self.order_no: str = order_no
        self.coas: List[Coa] = coas
        self.deli_date_path: str = deli_date_path
        self.isTest: bool = isTest
        self.destination: str = destination


    def show_coa_lot(self)-> None:
        print(self.order_no)
        for coa in self.coas:
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

        zip_path = r'{}/{}.zip'.format(self.deli_date_path, self.order_no) 
        with zipfile.ZipFile(zip_path ,'w') as z:
            find_count: int = 0 # 輸出ﾌｫﾙﾀﾞで見つけたcoaの数
            for coa in self.coas:
                lot = coa.lot
                for f in glob.glob(pdfPath + '*' + lot + '*' 
                                                  + self.order_no + '*'):
                    tmp = str(f).split(splitMoji)
                    zipName = tmp[-1]
                    # 'S6-UV382VB59S-T-R-EX_25090253T_2025911_長瀬産業/ﾌｧﾙﾃｯｸ_FB250535-1.pdf'
                        
                    tup_error = pc.hatumono_check(str(f))
                    if tup_error[0] == True:
                        print('「初物あるため、zipを中止しました」: ' 
                                                              + zipName)
                        with open(self.deli_date_path + '/log.txt', 'a') as f:
                            f.write('初物中止: ' + zipName + '\n')
                        break
                    elif tup_error[1] == True:
                        print('「errorがあるため、zipを中止しました」: '
                                                              + zipName)
                        with open(self.deli_date_path + '/log.txt', 'a') as f:
                            f.write('error中止: ' + zipName + '\n')
                        break
                    else:
                        z.write(f,zipName)
                        find_count += 1
                        break #lotと注番が一致するpdfが一個見つかったら抜ける。

            # 輸出ﾌｫﾙﾀﾞから見つけたcoaとself.coasとの数が一致したら、
            # success_ziped_coas(クラス変数)に追加
            if find_count == len(self.coas):
                DeliDateFolder.append_ziped_coa(self)


        
        with open(self.deli_date_path + '/log.txt', 'a') as f:
            f.write('\n')

