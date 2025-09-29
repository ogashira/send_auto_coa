import sys
from typing import List

class UserInterface(object):

    def __init__(self)-> None:
        pass

    def get_isTest(self)-> bool:
        args: List[str] = sys.argv
        if len(args) == 1:
            return False
        if args[1] == "test" or args[1] == "TEST":
            return True


    def get_delivery_date(self)-> str:
        while True:
            print('納入日を入力してください(例 : 20220930) / Returnで中止')
            delivery_date: str = input('納入日 : ')
            if not delivery_date:
                print('ﾌﾟﾛｸﾞﾗﾑを中止します')
                sys.exit()
                
            if (
                len(delivery_date) == 8 and
                2020 <= int(delivery_date[:4]) <= 2100 and
                1 <= int(delivery_date[4:6]) <= 12 and
                1 <= int(delivery_date[6:]) <= 31
                ):
                    break

            print('正しい年月日を入力してください')


        return delivery_date

