from struct import unpack
from collections import namedtuple

menu_index_len=10
menu_index_arry_tuple=namedtuple('menu_index_arry_tuple','m1 m2 m3')

class menu:
    def __init__(self,bytes):
        self.len,=unpack(">I",bytes[:4])
        print(self.len)
        self.indexes=self._GetIndex(bytes[4:])
        print(self.indexes)

    def _GetIndex(self,bytes):
        xxx =[bytes[i:i + menu_index_len] for i in range(0, menu_index_len*self.len, menu_index_len)]
        result=list()
        for i in xxx:
            m1,m2,m3=unpack(">IHI",i)
            result.append(menu_index_arry_tuple(hex(m1),hex(m2),hex(m3)))
        return result
