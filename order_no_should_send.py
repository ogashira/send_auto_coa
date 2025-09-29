from typing import List, Dict
from export_paint_list import ExportPaintList
from mail_info import MailInfo
from sent_order_no_folder import SentOrderNoFolder

class OrderNoShouldSend(object):

    def __init__(self, isTest: bool, delivery_date: str, 
                                                   deli_date_path: str) -> None:

        export_paint_list: ExportPaintList = ExportPaintList(delivery_date)
        self.export_paints: List[List[str]] = (
                                         export_paint_list.get_export_paints())
        mail_info: MailInfo = MailInfo(isTest) 
        self.mail_infos: List[List[str]] = mail_info.get_mail_infos()
        self.destinations: List[str] = mail_info.get_destinations()

        sent_order_no_folder: SentOrderNoFolder = SentOrderNoFolder(deli_date_path)
        self.sent_order_nos: List[str] = sent_order_no_folder.get_sent_order_nos()
        

    def get_should_send_coas(self)-> Dict[str, Dict[str, List[str]]]:
        '''
        should_send_coas = {'AHI832': {'タイ/小糸': [20250930T, 20250921T,...]}, 
                            'AHI855': {'タイ/小糸': [...]} }
        '''
        
        # self.destinationsでフィルターかけてDictへ変換
        filterd_dests: Dict[str, Dict[str, List[str]]] = {}
        for destination in self.destinations:
            for line in self.export_paints:
                dic_dest: Dict[str, List[str]] = {}
                filterd_dest: List[str] = []
                if destination in line:
                    if not line[1] in filterd_dests:
                        filterd_dest.append(str(line[2])) # lot
                        dic_dest[destination] = filterd_dest
                        filterd_dests[str(line[1])] = dic_dest
                    else:
                        filterd_dests[str(line[1])][destination].append(str(line[2]))

        if not filterd_dests:
            return filterd_dests

        # sent_order_nosでフィルターかけてDictへ変換
        if not self.sent_order_nos:
            return filterd_dests

        filterd_sents: Dict[str, Dict[str, List[str]]] = {} 
        for sent_order_no in self.sent_order_nos:
            for key, val in filterd_dests.items():
                if sent_order_no !=  key: # 送信済みでなかったら
                    filterd_sents[key] = val

        return filterd_sents
