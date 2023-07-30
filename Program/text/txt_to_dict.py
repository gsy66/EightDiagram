import json

def read_text(file_name):
    #将固定格式的txt文件转换为字典
    f = open(file_name,'r',encoding='utf-8')
    dict1={}
    for line in f:
        temp = line.strip().split(":")
        dict1[temp[0]]=temp[1]
    f.close()
    return dict1
def read_gua_yao(file_name):
    f=open("./text/guaci_yaoci.txt","r",encoding='utf-8')
    a=f.read().replace("'",'"')
    print(a)
    c=json.loads(a)
    return c

