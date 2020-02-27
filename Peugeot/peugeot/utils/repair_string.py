from struct import unpack
import os
import xmltodict

def get_string(file_path,id):
    path=file_path+"en_GB.DU8"
    data=open(path,'rb').read()
    head_bytes=data[:16]
    sig,pointer_start_addr,string_start_addr,string_cnt=unpack("<4I",head_bytes)
    start, = unpack("<I", data[pointer_start_addr + id * 4:pointer_start_addr + id * 4 + 4])
    end, = unpack("<I", data[pointer_start_addr + id * 4+4:pointer_start_addr + id * 4 + 8])
    return data[start:end]

def print_polux_data(file_name):
    data=open(file_name,'rb').read()
    newfile=file_name.replace("DU8","txt")
    f_out = open(newfile, "w")
    head_bytes=data[:16]
    sig,pointer_start_addr,string_start_addr,string_cnt=unpack("<4I",head_bytes)
    for i in range(string_cnt):
        begin_addr=pointer_start_addr+4*i
        xx,=unpack("<I",data[begin_addr:begin_addr+4])
        xxx,=unpack("<I",data[begin_addr+4:begin_addr+8])
        len=xxx-xx
        if(len):
            xxxx=str(data[xx:xx+len])
            xxxx=xxxx[1:]+"\n"
            f_out.write(xxxx)

def print_all_polux_data(dir_path="F:\my\Python\Peugeot\peugeot\lang_bin"):
    print(dir_path)
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            if file.find(".DU8")!=-1:
                xfile=os.path.join(root,file)
                print_polux_data(xfile)

def parse_string(xstr,lang_lib_path="./lang_bin"):
    xx=xstr.split(b"@")
    result=bytes()
    for x in xx:
        if len(x):
            if x[0]==70 or x[0]==80:
                temp=x[1:].split(b'-')
                temp[1]=temp[1].replace(b"\r\n",b"")
                file_path=os.path.join(lang_lib_path,bytes.decode(temp[1],"utf-8"))
                string_id=int(temp[0])
                str_val=get_string(file_path,string_id-1)
                result+=str_val
            elif x[0] == 10:
                result+=b'\n'
            else:
                result += x[1:]
    return result

def repair_xml_node_val(path,node):
    f=open(path,"rb")
    doc=f.readlines()
    f.close()
    length=0
    for x in doc:
        length+=1
    for i in range(length):
        len=doc[i].find(node)
        if len!=-1:
            ThesauRequest_val=doc[i][15:]
            repaired_val=node+parse_string(ThesauRequest_val)
            if repaired_val[-2:]==b"\r\n":
                repaired_val=repaired_val[:-2]
            repaired_val+=b" //"+ThesauRequest_val
            doc[i]=repaired_val
    os.remove(path)
    ff=open(path,"wb")
    ff.writelines(doc)
    ff.close()

def repair_xml_node_val1(path):
    f=open(path,"r")
    xml_data=f.read()
    f.close()
    xx=xmltodict.parse(xml_data)
    print(xx)

def trav_files(dir_path):
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            if file.find(".xml")!=-1:
                path=os.path.join(root,file)
                try:
                    repair_xml_node_val(path,b"<ThesauRequest>")
                except:
                    print(path)

def rename_files(dir_path):
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            if file.find(".s")!=-1:
                newname=file.replace(".s",".xml")
                os.rename(os.path.join(root,file),os.path.join(root,newname))


if __name__ == '__main__':
    # trav_files(r"F:\my\Python\Peugeot\peugeot\AWRoot\dtrd")
    # repair_xml_node_val(r"C:\Users\admin\Desktop\peugeot\tree\TeleXX\script_telexx_unlocking_ATM.xml",b"<ThesauRequest>")
    repair_xml_node_val1(r"C:\Users\admin\Desktop\peugeot\contextualisation.xml")
