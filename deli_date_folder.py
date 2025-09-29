from __future__ import annotations 
from typing import List
from mail_manage import MailManage

class DeliDateFolder:
    '''
    import annotationsで文字列で型を定義できる
    CoasShouldZipをインポートしてしまうと、循環参照で
    エラーになってしまうため。CoasShouldZipクラスには
    import DeliDateFolderがあるため。
    '''
    
    success_ziped_coas: List["CoasShouldZip"] 
    success_ziped_coas = []

    def __init__(self, mail_manage: MailManage)-> None:
        self.mail_manage: MailManage = mail_manage


    @classmethod
    def append_ziped_coa(cls, ziped_coa: "CoasShouldZip")->None:
        DeliDateFolder.success_ziped_coas.append(ziped_coa)


    def send_mail(self)-> List[List[str]]:
        success_send_mails: List[List[str]] = [] 
        for success_ziped_coa in DeliDateFolder.success_ziped_coas:
            destination = success_ziped_coa.destination
            order_no = success_ziped_coa.order_no
            deli_date_path = success_ziped_coa.deli_date_path
            success_send_mails.append( 
               self.mail_manage.send_mail(destination, order_no, deli_date_path)
                                     )
        return success_send_mails
                                                  


