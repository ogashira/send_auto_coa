import platform
from typing import List

class Coa(object):

    def __init__(self, order_no: str, lot: str)-> None:
        self.__order_no: str = order_no
        self.__lot: str = lot
    
    def show_lot(self)-> None:
        print('    ', end='') 
        print(self.__lot)

    def get_lot(self):
        return self.__lot
