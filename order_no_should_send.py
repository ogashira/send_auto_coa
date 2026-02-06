from re import I
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
        
        should_send_coas = {}
        for line in self.export_paints:
            order_no = str(line[1])
            lot = str(line[2])
            destination = None                                     
            for d in self.__destinations:                          
                if d in line:                                      
                    destination = d                                
                    break                                          
                                                                   
            if destination:                                        
                if order_no not in should_send_coas:               
                    should_send_coas[order_no] = {}                
                                                                   
                if destination not in should_send_coas[order_no]:  
                    should_send_coas[order_no][destination] = []   
                                                                   
                should_send_coas[order_no][destination].append(lot)
                                                                   
        return should_send_coas                                    


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
        print()
        print(f'({date_deli} に送信が必要なCOA)')
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
            f.write('\n')
            f.write(f'({date_deli} に送信が必要なCOA)\n')
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
        print(f'(既に送信済みの注番)')
        for no in self.__sent_order_nos:
            print(no)
        print('\n')

        with open(log_path, 'a') as f:
            f.write(f'(既に送信済みの注番)\n')

            num:int = 1
            for no in self.__sent_order_nos:
                f.write(f'{num}. {no}\n')
            f.write('\n\n')


    def show_should_send_coas_thisTime(self, log_path:str )-> None:
        print(f'(未送信のため送信が必要なCOA)')
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
            f.write(f'(未送信のため送信が必要なCOA)\n')
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

    def show_target_for_yet(self, log_path: str, 
                            success_send_mails:List[List[str]])-> None:
        #success_send_mails = [['AHI832', 'タイ/小糸'], ['AHI855', 'タイ小糸']] 

        success_orderNos: List[str] = []
        for line in success_send_mails:
            success_orderNos.append(line[0]) #['AHI832', 'AHI855'...]

        targets_for_yet: List[List[str]] = [] #[['AHI832', 'タイ/小糸'],..]
        for orderNo, v in self.__should_send_coas_thisTime.items():
            target_for_yet: List[str] = []
            for destination in v.keys():
                if not orderNo in success_orderNos:
                    target_for_yet.append(orderNo)
                    target_for_yet.append(destination)
                    targets_for_yet.append(target_for_yet)
        
            
        print(f'(未だに送信できていない向先)')
        num: int = 1
        for line in targets_for_yet:
            print(f'{num}. {line[0]}, {line[1]}')
            num += 1
        print('\n')

        with open(log_path, 'a') as f:
            f.write(f'(未だに送信出来ていない向先)\n')
            num: int = 1
            for line in targets_for_yet:
                f.write(f'{num}. {line[0]}, {line[1]}\n')
                num += 1
            f.write('\n\n')
