import os
def GetStartAddr(fdata,sig):
    index=0
    for i in range(0,len(fdata)):
        if fdata[i]==0:
            tStr = fdata[index:i]
            index = i + 1
            if tStr==sig:
                break
    return i+1

def GetQT(fdata,path):
    QTfile = open(path, "wb+")
    index=GetStartAddr(fdata,b"<QT>")
    cnt=0
    for i in range(index,len(fdata)):
        if fdata[i]==0:
            tStr = fdata[index:i]
            if tStr==b"</QT>":
                break
            if cnt!=3:
                QTfile.write(tStr+b"    ")
                cnt+=1
                index=i+1
            if cnt==3:
                QTfile.write(b"\x0d\x0a")
                cnt=0

def GetQV(fdata,path):
    QVfile = open(path, "wb+")
    index = GetStartAddr(fdata, b"<QV>")
    cnt = 0
    for i in range(index,len(fdata)):
        if fdata[i]==0:
            tStr = fdata[index:i]
            if tStr==b"</QV>":
                break
            if cnt!=4:
                QVfile.write(tStr+b"    ")
                cnt+=1
                index=i+1
            if cnt==4:
                QVfile.write(b"\x0d\x0a")
                cnt=0

def BytesToStr(bytes):
    for b in bytes:
        xx = int.from_bytes(bytes ,byteorder='little', signed=False)
        xx="0x%04X  "%xx
    return xx

def GetVQ(fdata,path):
    VQfile = open(path, "wb+")
    index = GetStartAddr(fdata, b"<VQ>")+1
    cnt=int.from_bytes(fdata[index:index+2], byteorder='little', signed=False)
    index+=2
    for i in range(cnt):
        for j in range(21):
            tBytes=BytesToStr(fdata[index:index+2])
            VQfile.write(tBytes.encode(encoding="utf-8"))
            index+=2
        VQfile.write(b"\x0d\x0a")

def ExpVehicles(path=r"C:\Users\admin\Desktop\FordData"):
    fdata = open(path+"\Vehicles", "rb").read()
    OutPath=path+"\VehiclesOut"
    if not os.path.exists(OutPath):
        os.makedirs(OutPath)
    GetQT(fdata, OutPath+"\QT.txt")
    GetQV(fdata, OutPath+"\QV.txt")
    GetVQ(fdata, OutPath+"\VQ.txt")

















