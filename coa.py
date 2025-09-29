import platform
from typing import List

class Coa(object):

    def __init__(self, order_no: str, lot: str)-> None:
        self.order_no: str = order_no
        self.lot: str = lot
    
    def show_lot(self)-> None:
        print('    ', end='') 
        print(self.lot)

