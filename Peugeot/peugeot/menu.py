import os
tree_path=r'C:\Users\admin\Desktop\peugeot\tree'
output_path=r'C:\Users\admin\Desktop\peugeot\out'
out_ecu_path=r'C:\Users\admin\Desktop\peugeot\out\ecu'
ve_cnt = 0



def write_vehicle_tab():
    f_v_menu=open(output_path+r'\vehicle.txt','w')
    ve_cnt=0
    for root, dirs, files in os.walk(tree_path+r'\vehicle'):
        for dir in dirs:
            ve_cnt+=1
            f_v_menu.write("0x%02X"%ve_cnt+" "+dir+"\n")
        return



def write_ecu_tabs():
    vehicle_list=list()
    v_path=tree_path + r'\vehicle'
    for root, dirs, files in os.walk(v_path):
        for dir in dirs:
            ecu_path=os.path.join(v_path,dir)
            out_path=os.path.join(out_ecu_path,dir)+"_ECU.txt"
            f = open(out_path, "w")
            for root, dirs, files in os.walk(ecu_path):
                ecu_cnt = 0
                for dir in dirs:
                    ecu_cnt+=1
                    f.write("0x%02X"%ecu_cnt+" "+dir+"\n")
                break
        break

def rename_s_xml():
    for root, dirs, files in os.walk(tree_path):
        for file in files:
            if file.find(".s")!=-1:
                newname=file.replace(".s",".xml")
                os.rename(os.path.join(root,file),os.path.join(root,newname))


def trav_and_create_all():
    write_vehicle_tab()
    write_ecu_tabs()


if __name__ == '__main__':
    trav_and_create_all()