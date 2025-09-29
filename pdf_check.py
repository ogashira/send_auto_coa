#! python
# -*- coding:utf-8 -*-

from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.layout import LAParams
from io import StringIO
import platform


class PdfCheck(object):
    '''
    pdfﾌｧｲﾙをzipでまとめる前に、ﾁｪｯｸするｸﾗｽ。
    hatumono_check: coaに「初物要ﾁｪｯｸ！」が記載されていないかをﾁｪｯｸする
    Falseが返れば問題なしで、zipにしてもよい

                                                programming by oga
    '''

    def __init__(self):
        pass


    def hatumono_check(self, file_name):
        '''
        path付きのfileﾈｰﾑが引数としてわたってくる
        '''

        # bool_hatumonoをreturnする。Trueならば、初物要ﾁｪｯｸの記載あり。
        bool_hatumono = False
        bool_ref = False

        # 標準組込み関数open()でモード指定をbinaryでFileオブジェクトを取得
        '''
        if platform.system() == 'Windows':
            file_path = '//192.168.1.247/共有/営業課ﾌｫﾙﾀﾞ/testreport/輸出/'
        elif platform.system() == 'Linux':
            file_path = './zipTest/'

        file_path_name = file_path + file_name
        '''
        fp = open(file_name, 'rb')

        # 出力先をPythonコンソールするためにIOストリームを取得
        outfp = StringIO()


        # 各種テキスト抽出に必要なPdfminer.sixのオブジェクトを取得する処理

        rmgr = PDFResourceManager() # PDFResourceManagerオブジェクトの取得
        lprms = LAParams()          # LAParamsオブジェクトの取得
        device = TextConverter(rmgr, outfp, laparams=lprms)    # TextConverterオブジェクトの取得
        iprtr = PDFPageInterpreter(rmgr, device) # PDFPageInterpreterオブジェクトの取得

        # PDFファイルから1ページずつ解析(テキスト抽出)処理する
        for page in PDFPage.get_pages(fp):
            iprtr.process_page(page)

        text = outfp.getvalue()  # Pythonコンソールへの出力内容を取得

        outfp.close()  # I/Oストリームを閉じる
        device.close() # TextConverterオブジェクトの解放
        fp.close()     #  Fileストリームを閉じる


        if '初物 要チェック' in text:
            bool_hatumono = True

        if '#REF!' in text:
            bool_ref = True

        tup_error = (bool_hatumono, bool_ref)

        return tup_error
