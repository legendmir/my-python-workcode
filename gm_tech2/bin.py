from struct import unpack
from menu import menu
from en_string import en_string
from collections import namedtuple
from handle_mem_access_data import memdata


head_size=24
table_size=38
menu_addr=0x1c00000

en_string1_start=0x104000C
en_string1_end=0x10A10B7
en_string2_start=0x625da0
en_string2_end=0x65D96A


class table:
    def __init__(self,bytes):
        self.size=table_size
        self.file_name,\
        self.page_sn,\
        self.mask_start_addr,\
        self.content_size,\
        self.unknown,\
        self.m5,self.m6,self.m7,self.m8,self.m9,self.m10 = unpack(">14sH2I7H", bytes)

        self.file_addr=self.page_sn*0x100000+self.mask_start_addr-0x200000
        self.file_size = self.content_size
        self.file_end_addr = self.file_addr+self.file_size


    def __str__(self):
        return "file_name=%s,page_sn=0x%04X,mask_start_addr=0x%08X,content_size=0x%08X,unknown=0x%04X,m5=0x%04X,m6=0x%04X,m7=0x%04X,m8=0x%04X,m9=0x%04X,m10=0x%04X\n"\
               %(self.file_name.decode("utf-8"),self.page_sn,self.mask_start_addr,self.content_size,self.unknown,self.m5,self.m6,self.m7,self.m8,self.m9,self.m10)
    def get_file_loc(self):
        return self.file_name.decode("utf-8"),self.file_addr,self.file_end_addr


class head:
    def __init__(self,bytes):
        newbytes=self._xx(bytes[:head_size])
        self.size=head_size
        self.name,self.m1,self.m2,self.table_len,self.m4,self.m5,self.nation=unpack(">4s5H10s",newbytes)
        self.tables=[table(bytes[head_size:][i:i + table_size]) for i in range(0, table_size*self.table_len, table_size)]

    def __str__(self):
        return "name=%s,m1=0x%04X,m2=0x%04X,table_len=0x%04X,m4=0x%04X,m5=0x%04X,nation=%s"%\
               (self.name.decode("utf-8"),self.m1,self.m2,self.table_len,self.m4,self.m5,self.nation.decode("utf-8"))

    def _xx(self,xbytes):
         newbytes=list()
         for i in xbytes:
            if i==0xff:
                newbytes.append(0x20)
            else:
                newbytes.append(i)
         return bytes(newbytes)



class bin:
    def __init__(self,bytes):
        self.head=head(bytes)
        self.file_locations=self._get_file_locs()
        self.string_bytes1=bytes[en_string1_start:en_string1_end]
        self.string_bytes2=bytes[en_string2_start:en_string2_end]
        self.strings = en_string(self.string_bytes1,self.string_bytes2).get_strings()
        self.addrs=en_string(self.string_bytes1,self.string_bytes2).get_str1_addrs()
        # self.strings2=en_string(self.string_bytes1,self.string_bytes2).get_strings2()
        # print(self.file_locations)
        # self.menu=menu(bytes[menu_addr:])
    #     r"E:\Job Project\GM\Tech2\string.txt"




    def _get_file_locs(self):
        result =list()
        for i in self.head.tables:
            result.append(i.get_file_loc())
        return result

    def print_origin_head(self,path):
        f=open(path,"w")
        f.write(str(self.head)+"\n")
        for table in self.head.tables:
            f.write(str(table))

    def get_file_name_by_addr(self,addr):
        for i in self.file_locations:
            if addr>=i[1] and addr <=i[2]:
                return i[0]
        return ""

    def get_per_content(self,bytes,offset,len):
        result=bytes[offset:offset+len]
        result = ' '.join(['%02x' % x for x in result])
        return result

    def print_mem_info(self,in_path,out_path):
        out=open(out_path,"w")
        xx=memdata(in_path).handled_info
        for i in xx:
            file_name=self.get_file_name_by_addr(int(i[0],16))
            print(i[1])
            content=self.get_per_content(self.xbytes,int(i[0],16),i[1])
            xxxx="0x"+i[0]+","+hex(i[1])+","+file_name+","+content+"\n"
            out.write(xxxx)

