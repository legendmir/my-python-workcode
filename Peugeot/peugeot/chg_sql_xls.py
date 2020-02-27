import firebirdsql
from pyexcel_xls import save_data
from peugeot.utils.repair_string import parse_string

data_type={496:"INTERGER",500:"BOOL",448:"VARCHAR",482:"FLOAT",452:"CHAR",520:"BINARY"}


GPC = firebirdsql.connect(
    host='localhost',
    database='E:/Job Project/Peugeot/AWRoot/dtrd/comm/data/GPC.FDB',
    port=3050,
    user='SYSDBA',
    password='masterkey'
)

DSD = firebirdsql.connect(
    host='localhost',
    database='E:/Job Project/Peugeot/AWRoot/dtrd/comm/data/DSD.FDB',
    port=3050,
    user='SYSDBA',
    password='masterkey'
)

def get_sqls(path):
    f=open(path,"r")
    sql=list()
    text=f.readlines()
    i=0
    while i<len(text):
        persql=str()
        if not text[i][0].isdigit():
            persql=text[i]
            while i+1<len(text):
                if not text[i+1][0].isdigit():
                    persql+=text[i+1]
                    i+=1
                else:
                    break
        if len(persql):
            sql.append(persql)
        i+=1
    sql2 = sorted(set(sql), key=sql.index)
    return sql2


def get_per_sql_list(db,sql):
    cur = db.cursor()
    cur = db.cursor()
    cur.execute(sql)
    xsql=sql.replace('\n',' ')
    sheet=list()
    head=list()
    head.append(xsql)
    name = [x[0] for x in cur.description]
    xtype = [data_type[x[1]] for x in cur.description]
    sheet.append(head)
    sheet.append(name)
    sheet.append(xtype)
    for xx in cur.fetchall():
        xxx = list()
        for i in range(len(xx)):
            if isinstance(xx[i],str) and len(xx[i]):
                if xx[i][0]=='@':
                    t=parse_string(str.encode(xx[i],"utf-8"))
                    xxx.append(bytes.decode(t,"utf-8"))
                    continue
            xxx.append(xx[i])
        print(xxx)
        sheet.append(xxx)
    cur.close()
    return sheet


# 写Excel数据, xls格式
def save_xls_file(sqls,path):
    # sheet表的数据
    data=dict()
    all_data=list()
    for sql in sqls:
        try:
            sheet_list=get_per_sql_list(GPC,sql)
        except:
            sheet_list = get_per_sql_list(DSD, sql)
        all_data+=sheet_list
    data.update({"Sheet1": all_data})
    # 保存成xls文件
    save_data(path, data)


def get_output(path):
    sqls = get_sqls(path)
    newpath=path.replace("txt","xls")
    save_xls_file(sqls,newpath)


if __name__ == '__main__':
    get_output(r"C:\Users\admin\Desktop\peugeot\hook\AWFIn_HookOut.txt")







