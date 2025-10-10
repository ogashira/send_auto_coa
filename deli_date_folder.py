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
                                                  


