from struct import unpack


class en_string:
    def __init__(self,xbytes1,xbytes2):
        self.xbytes1=xbytes1
        self.xbytes2=xbytes2
        self.str2_list=list()
        self.str1_addrs=list()

    def get_strings_by_id(self,id):
        for xx in reversed(self.str2_list):
            if xx[0]==id:
                return xx[1]

    def get_str1_addrs(self):
        i = 0
        while i < len(self.xbytes1):
            while i < len(self.xbytes1) and self.xbytes1[i] != 0:
                if self.xbytes1[i] == 3:
                    i += 3
                else:
                    i += 1
            i += 1
            self.str1_addrs.append(i+12)
        return self.str1_addrs

    def get_string2_list(self):
        per_bytes = bytes()
        i = 0
        xid=0
        id=0
        while i<len(self.xbytes2):
            while i<len(self.xbytes2) and self.xbytes2[i]!= 0:
                if self.xbytes2[i] == 3:
                    id, = unpack(">H", self.xbytes2[i+1:i + 3])
                    result=self.get_strings_by_id(id)
                    per_bytes+=result
                    i += 3
                else:
                    per_bytes+=self.xbytes2[i].to_bytes(length=1,byteorder='big',signed=False)
                    i += 1

            self.str2_list.append((xid,per_bytes))
            xid +=1
            per_bytes=b""
            i += 1
        self.str2_list=self.str2_list[:-1]

    def get_string1_list(self):
        result_list=list()
        per_bytes = bytes()
        i = 0
        id = 0
        while i < len(self.xbytes1):
            while i < len(self.xbytes1) and self.xbytes1[i] != 0:
                if self.xbytes1[i] == 3:
                    id, = unpack(">H", self.xbytes1[i + 1:i + 3])
                    result = self.get_strings_by_id(id)
                    per_bytes += result
                    i += 3
                else:
                    per_bytes += self.xbytes1[i].to_bytes(length=1, byteorder='big', signed=False)
                    i += 1
            # print(hex(i+9))
            result_list.append((i+9,per_bytes))
            per_bytes = b""
            i += 1
        return result_list

    def get_strings2(self):
        self.get_string2_list()

        return self.str2_list


    def get_strings(self):
        self.get_string2_list()
        return self.get_string1_list()




