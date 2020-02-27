import firebirdsql
import xmltodict

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

def GetSql(path):
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

def get_per_xmlnode(db,sql):
    cur = db.cursor()
    cur=db.cursor()
    cur.execute(sql)
    xsql = sql[:len(sql) - 1]
    xsql=xsql.replace('\n',' ')
    node_dict={
            'Sql': '"' + xsql + '"',
            'Properties': {},
            'Rowdata': {}
    }
    field=list()
    node_properties = node_dict['Properties']
    for xx in cur.description:
        field.append('name='+'"'+xx[0]+'"'+" type="+'"'+data_type[xx[1]]+'"')
    node_properties['FIELD ']=field
    node_rowdata = node_dict['Rowdata']
    row=list()
    for xx in cur.fetchall():
        onerow = str()
        for i in range(len(xx)):
            onerow+=cur.description[i][0]+'="'+str(xx[i])+'" '
        row.append(onerow)
    node_rowdata['ROW']=row
    cur.close()
    return node_dict

def GetXml(sqls):
    node_list=list()
    for sql in sqls:
        try:
            per_node = get_per_xmlnode(GPC, sql)
        except:
            per_node = get_per_xmlnode(DSD, sql)
        node_list.append(per_node)

    xml_dict={
        'DATA': {
            'NODE':{}
        },
    }
    xml_dict['DATA']['NODE']=node_list
    return xml_dict

def get_output(path):
    sqls = GetSql(path)
    newpath=path.replace("txt","xml")
    f = open(newpath, "w")
    mydict=dict()
    mydict = GetXml(sqls)
    f.write(xmltodict.unparse(mydict, pretty=False))



if __name__ == '__main__':
    get_output(r"E:\Job Project\Peugeot\hook\MCC_HookOut.txt")
    get_output(r"E:\Job Project\Peugeot\hook\AWFIn_HookOut.txt")
