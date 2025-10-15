from __future__ import annotations 
from typing import List

class DeliDateFolder:
    '''
    import annotationsで文字列で型を定義できる
    CoasShouldZipをインポートしてしまうと、循環参照で
    エラーになってしまうため。CoasShouldZipクラスには
    import DeliDateFolderがあるため。
    '''
    
    success_ziped_coas: List["CoasShouldZip"] 
    success_ziped_coas = []

    def __init__(self)-> None:
        pass


    @classmethod
    def append_ziped_coa(cls, ziped_coa: "CoasShouldZip")->None:
        DeliDateFolder.success_ziped_coas.append(ziped_coa)


    def send_mail(self)-> List[List[str]]:
        success_send_mails: List[List[str]] = [] 
        for success_ziped_coa in DeliDateFolder.success_ziped_coas:
            success_send_mails.append( success_ziped_coa.send_mail())
        return success_send_mails
                                                  

    def show_success_ziped_coas(self, log_path)-> None:
        print(f'(zipに成功したCOA)')
        num: int = 1
        for coas_should_zip in DeliDateFolder.success_ziped_coas:
            coas_should_zip.show_orderNo_destination(num)
            num += 1
        print('\n')

        with open(log_path, 'a') as f:
            f.write(f'(zipに成功したCOA)\n')

        num: int = 1
        for coas_should_zip in DeliDateFolder.success_ziped_coas:
            coas_should_zip.fwrite_orderNo_destination(log_path, num)
            num += 1

        with open(log_path, 'a') as f:
            f.write('\n\n')

