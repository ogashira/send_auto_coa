import pprint
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
        self.__mail_infos: List[List[str]] = mail_info.get_mail_infos()
        self.__destinations: List[str] = mail_info.get_destinations()

        sent_order_no_folder: SentOrderNoFolder = SentOrderNoFolder(deli_date_path)
        self.__sent_order_nos: List[str] = sent_order_no_folder.get_sent_order_nos()

        # この納期日に送信が必要なcoa
        self.__should_send_coas: Dict[str, Dict[str, List[str]]] = self.get_should_send_coas()

        # 送信済みを除いた、今回の実行で送信が必要なcoa
        self.__should_send_coas_thisTime: Dict[str, Dict[str, List[str]]] = self.get_should_send_coas_thisTime()
        

    def isShouldSendCoas(self)-> bool:
        '''
        Controlから今日送信しなければいけないCoaがあるのかどうかを確認するために呼ばれる
        '''
        return len(self.__should_send_coas) > 0 
        # self.export_paints == True だと、全てFalseになってしまう？？？？
        

    def get_should_send_coas(self)-> Dict[str, Dict[str, List[str]]]:
        '''
        この納期日に送信が必要なcoa
        should_send_coas = {'AHI832': {'タイ/小糸': [20250930T, 20250921T,...]}, 
                            'AHI855': {'タイ/小糸': [...]} }
        '''
        
        # self.__destinationsでフィルターかけてDictへ変換
        self.__should_send_coas = {}
        for destination in self.__destinations:
            dic_dest: Dict[str, List[str]] = {}
            filterd_dest: List[str] = []
            for line in self.export_paints:
                if destination in line:
                    if not line[1] in self.__should_send_coas:
                        filterd_dest.append(str(line[2])) # lot
                        dic_dest[destination] = filterd_dest
                        self.__should_send_coas[str(line[1])] = dic_dest
                    else:
                        self.__should_send_coas[str(line[1])][destination].append(str(line[2]))

        return self.__should_send_coas


    def get_should_send_coas_thisTime(self)-> Dict[str, Dict[str, List[str]]]:
        '''
        送信済みを除いた、今回の実行で送信が必要なcoa
        '''
        self.__should_send_coas_thisTime = {}
        # __sent_order_nosでフィルターかけてDictへ変換
        if not self.__sent_order_nos:
            self.__should_send_coas_thisTime = self.__should_send_coas
            return self.__should_send_coas_thisTime

        order_nos: List[str] = list(self.__should_send_coas.keys())
        for order_no in order_nos:
            if not order_no in self.__sent_order_nos: # 送信済みでなかったら
                self.__should_send_coas_thisTime[order_no] = self.__should_send_coas[order_no]


        return self.__should_send_coas_thisTime


    def show_should_send_coas(self, log_path:str, date_deli:str)-> None:
        print(f'{date_deli} に送信が必要なCOA')
        num:int = 1
        for orderNo, v in self.__should_send_coas.items():
            myStr: str = ""
            for destination, v2 in v.items(): 
                myStr = f'{num}. {orderNo}, {destination}, '
                for lot in v2:
                    myStr += f'{lot}, '
            print(f'{myStr}')
            num += 1

        print('\n')

        with open(log_path, 'a') as f:
            f.write(f'{date_deli} に送信が必要なCOA\n')
            num:int = 1
            for orderNo, v in self.__should_send_coas.items():
                myStr: str = ""
                for destination, v2 in v.items(): 
                    myStr = f'{num}. {orderNo}, {destination}, '
                    for lot in v2:
                        myStr += f'{lot}, '
                f.write(f'{myStr}\n')
                num += 1

            f.write('\n\n')



    def show_sent_order_nos(self, log_path:str)-> None:
        print(f'既に送信済みの注番')
        for no in self.__sent_order_nos:
            print(no)
        print('\n')

        with open(log_path, 'a') as f:
            f.write(f'既に送信済みの注番\n')

            num:int = 1
            for no in self.__sent_order_nos:
                f.write(f'{num}. {no}\n')
            f.write('\n\n')


    def show_should_send_coas_thisTime(self, log_path:str )-> None:
        print(f'未送信のため送信が必要なCOA')
        num:int = 1
        for orderNo, v in self.__should_send_coas_thisTime.items():
            myStr: str = ""
            for destination, v2 in v.items(): 
                myStr = f'{num}. {orderNo}, {destination}, '
                for lot in v2:
                    myStr += f'{lot}, '
            print(f'{myStr}')
            num += 1

        print('\n')

        with open(log_path, 'a') as f:
            f.write(f'未送信のため送信が必要なCOA\n')
            num:int = 1
            for orderNo, v in self.__should_send_coas_thisTime.items():
                myStr: str = ""
                for destination, v2 in v.items(): 
                    myStr = f'{num}. {orderNo}, {destination}, '
                    for lot in v2:
                        myStr += f'{lot}, '
                f.write(f'{myStr}\n')
                num += 1

            f.write('\n\n')

