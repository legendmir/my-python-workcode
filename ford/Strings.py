import os
def ExpString(path=r"C:\Users\admin\Desktop\FordData"):
    fdata=open(path+"\Strings","rb").read()
    OutPath=path+"\StringOut"
    if not os.path.exists(OutPath):
        os.makedirs(OutPath)
    OutPath+="\StringOut.txt"
    fString=open(OutPath,"w+")
    OneStr=""
    addr=0
    sAddr=""
    for byte in fdata:
        if  byte!=0 \
            and byte!=0xa0\
            and byte!=0xc1:
            OneStr+=chr(byte)
        else:
            if OneStr != "":
                sAddr="0x%08X    "%(addr-len(OneStr))
                fString.write(sAddr)
                fString.write(OneStr)
                fString.write(b"\x0d\x0a".decode(encoding="utf-8"))
            OneStr=""
        addr+=1







