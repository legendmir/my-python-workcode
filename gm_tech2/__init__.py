from bin import bin
from struct import unpack

path_NAO=r"E:\Job Project\GM\Tech2\North American Operations.bin"
bin_NAO=open(path_NAO,"rb").read()
# path_CN1=r"E:\Job Project\GM\Tech2\China2.bin"
# bin_CN1=open(path_CN1,"rb").read()
# NA0=bin(bin_NAO)
# NA0.print_origin_head(r"E:\Job Project\GM\Tech2\output\head_NA.txt")
# bin(bin_NAO).print_mem_info(r"E:\Job Project\GM\Tech2\output\tech2hook.txt",r"E:\Job Project\GM\Tech2\output\handled.txt")
xx=bin(bin_NAO)



f1=open(r"E:\Job Project\GM\Tech2\string.txt","wb")


id=[12]+xx.addrs

for i in range(len(xx.strings)):
    f1.write(b"0x%08X   "%id[i]+xx.strings[i][1]+b"\x0d\x0a")

# for x in xx.strings:
#     f1.write(b"0x%04X   "%x[0]+x[1]+b"\x0d\x0a")


