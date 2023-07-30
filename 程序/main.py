#!-*- coding:utf-8 -*-
import sys, random,json
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QGraphicsScene,QWidget, QLabel,QDialog
from PyQt5.QtGui import QPixmap, QImage
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer, pyqtSignal
from PyQt5.uic import loadUi

from 万年历.t2 import MingGua

eight_gua={
    "111":"乾",
    "000":"坤",
    "110":"巽",#xun
    "001":"震",
    "010":"坎",
    "101":"离",
    "100":"艮",
    "011":"兑",
}
eight_gua2={
    "乾":"111",
    "坤":"000",
    "巽":"110",#xun
    "震":"001",
    "坎":"010",
    "离":"101",
    "艮":"100",
    "兑":"011",
}
def NameOfGua(gua,guaming):
    msg=eight_gua[''.join(gua[0:3])]+"上"+eight_gua[''.join(gua[3:6])]+'下'
    msg2=guaming[msg].split(" ") 
    #卦辞
    name_gua=msg2[1]
    return name_gua
def yao_random():
    a = [random.randint(6,9) for i in range(0,6)]
    b = [str(x%2) for x in a]
    b.reverse()
    return a,b
def hu_gua(a):
    b=[]#存储显示信息，字符串1和0卦象从上到下
    c=[]#存储互卦基础详细信息
    for i in range(1,4):
        b.append(str(a[i]%2))
        c.append(a[i])
    for i in range(2,5):
        b.append(str(a[i]%2))
        c.append(a[i])
    b.reverse()
    return c,b
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
    f=open(file_name,"r",encoding='utf-8')
    a=f.read().replace("'",'"')
    c=json.loads(a)
    return c
def biangua(a):
    bian=[]
    for i in range(len(a)):
        if a[i]==9:
            bian.append(6)
        elif a[i]==6:
            bian.append(9)
        else:
            bian.append(a[i])
    b=[str(x%2) for x in bian]
    b.reverse()
    return bian,b
def yibianyao(beng):
    #宜变之爻
    dayan_num=55
    num0=sum(beng)
    dif = dayan_num-num0
    list0=[1,2,3,4,5,6,5,4,3,2]
    yao=list0[dif%len(list0)]
    return yao
def jiegua(gua_ben,gua_bian,gua_i1,guai_2,guaci,guaming):
    yao=yibianyao(gua_ben)
    name_gua_ben=NameOfGua(gua_i1,guaming)
    name_gua_bian=NameOfGua(guai_2,guaming)
    flag=[0,0,0,0,0,0]  #可变之爻的数量
    sum_yao=0
    for i in range(len(gua_ben)):
        if gua_ben[i]==9 or gua_ben[i]==6:
            flag[i]=1
            sum_yao+=1
    if flag[yao-1]==1:
        #宜变之爻为可变之爻，以本卦变卦爻辞占之
        msg=guaci[name_gua_bian]["爻"][yao-1]
        #print("宜变之爻为可变之爻，以本卦变卦爻辞占之")
        #print(msg)
        return [msg[1],msg[2]]
    else:
        #宜变宜变之爻为不可变之爻
        if sum_yao<3:
            #可变之爻数少于不可变之爻数,以本卦卦辞占之
            msg=guaci[name_gua_ben]["卦"]
            #print("以本卦卦辞占之")
            #print(msg)
            return [msg[0],msg[1],msg[2]]
        elif sum_yao==3:
            #可变之爻数等于不可变之爻数,以本卦之卦卦辞合占之
            msg=guaci[name_gua_ben]["卦"]
            msg2=guaci[name_gua_bian]["卦"]
            #print("以本卦之卦卦辞合占之")
            #print("本卦：{}变卦：{}".format(msg,msg2))
            return ["本卦：{}变卦：{}".format(msg[0],msg2[0]),"本卦：{}，变卦：{}".format(msg[1],msg2[1]),"本卦：{}变卦：{}".format(msg[2],msg2[2])]
        elif sum_yao>3:
            #可变之爻数少于不可变之爻数,以之卦卦辞占之
            msg2=guaci[name_gua_bian]["卦"]
            #print("以之卦卦辞占之")
            #print(msg2)
            return [msg2[0],msg2[1],msg2[2]]
    

class mainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUI()
        self.dict_init()
        self.showimg() 
        self.ChildDialog = ChildWin()
        self.MingGDialog = MingGuaWin()
        gua_ben,gua_ben_show=yao_random()
        self.pushButton.clicked.connect(self.OneStep)
        self.pushButton_2.clicked.connect(self.child)
        self.checkBox.setChecked(True)
        self.MingG.triggered.connect(self.MingInput)
    def setupUI(self):
        loadUi('./ui/img2.ui',self)

    def child(self):
        self.ChildDialog.show()
        self.ChildDialog._signal.connect(self.getData)
    
    def MingInput(self):
        self.MingGDialog.show()
    def getData(self,yao):
        #self.lineEdit.setText(parameter)
        a = [int(yao[i]) for i in range(0,6)]
        b = [str(x%2) for x in a]
        b.reverse()
        self.show_text(a,b)

    def dict_init(self):
        self.guaming=read_text(file_name="./text/guaming.txt")
        self.gua_yao_ci=read_gua_yao(file_name="./text/guaci_yaoci.txt")

    def OneStep(self):
        gua_ben,gua_ben_show=yao_random()
        self.show_text(gua_ben,gua_ben_show)

    def showimg(self):
        self.lu="./64_img/" +'bagua'+".jpg"
        self.pm=QPixmap(self.lu)
        self.label_ben.setPixmap(self.pm)
        #self.label.move(self.width()/2-self.label.width()/2,50)
        self.label_ben.setScaledContents(True)
        self.label_bian.setPixmap(self.pm)
        self.label_bian.setScaledContents(True)
        self.label_hu.setPixmap(self.pm)
        self.label_hu.setScaledContents(True)
        self.textBrowser.append("<h1>欢迎使用该软件</h1>")
        self.textBrowser.append("<h1>软件版本1.3.0</h1>")
        self.textBrowser.append("<h1>最新更新内容：更新了命卦的计算与显示，通过左上角下拉菜单可进入命卦计算子窗口，再选择出生年月与时辰即可成命卦</h1>")
        #self.show()

    def show_text(self,gua_ben,gua_ben_show):
        if(self.checkBox.isChecked()==True):
            print(1)
        else:
            print(0)
        gua_hu,gua_hu_show=hu_gua(gua_ben)
        gua_bian,gua_bian_show=biangua(gua_ben)
        self.lu = "./64_img/" +''.join(gua_ben_show)+".jpg"
        self.hu="./64_img/" +''.join(gua_hu_show)+".jpg"
        self.bian="./64_img/" +''.join(gua_bian_show)+".jpg"
        self.pm = QPixmap(self.lu)
        self.hm = QPixmap(self.hu)
        self.im = QPixmap(self.bian)
        self.label_ben.setPixmap(self.pm)
        self.label_hu.setPixmap(self.hm)
        self.label_bian.setPixmap(self.im)
        self.textBrowser.clear()
        msg=eight_gua[''.join(gua_ben_show[0:3])]+"上"+eight_gua[''.join(gua_ben_show[3:6])]+'下'
        msg2=eight_gua[''.join(gua_hu_show[0:3])]+"上"+eight_gua[''.join(gua_hu_show[3:6])]+'下'
        msg3=eight_gua[''.join(gua_bian_show[0:3])]+"上"+eight_gua[''.join(gua_bian_show[3:6])]+'下'
        name_ben=NameOfGua(gua_ben_show,self.guaming)
        name_bian=NameOfGua(gua_bian_show,self.guaming)
        beg=self.gua_yao_ci[name_ben]["卦"]
        big=self.gua_yao_ci[name_ben]["卦"]
        #显示卦名
        self.textBrowser.append("<h1>"+self.guaming[msg]+"<\h1>")
        self.textBrowser.append("<h1>"+self.guaming[msg2]+"<\h1>")
        self.textBrowser.append("<h1>"+self.guaming[msg3]+"<\h1>")
        #显示卦辞
        lastmsg=jiegua(gua_ben,gua_bian,gua_ben_show,gua_bian_show,self.gua_yao_ci,self.guaming)
        self.textBrowser.append("<h1>占词：<\h1>")
        if(self.checkBox.isChecked()==True):
            print(1)
            for m in lastmsg:
                self.textBrowser.append("<h1>"+m+"<\h1>")
        else:
            print(0)
            self.textBrowser.append("<h1>"+lastmsg[0]+"<\h1>")

class ChildWin(QDialog):
    _signal = QtCore.pyqtSignal(str)
    def __init__(self):
        super().__init__()
        self.setupUI()
        self.pushButton.clicked.connect(self.yaoshu)
    def setupUI(self):
        loadUi('./ui/Childwindow.ui',self)
    
    def yaoshu(self):
        data_str = self.lineEdit.text()
        self._signal.emit(data_str)

class MingGuaWin(QDialog):
    def __init__(self):
        super().__init__()
        self.setupUI()
        self.pushButton.clicked.connect(self.to_main)
        self.dateTimeEdit.dateTimeChanged.connect(self.onDateTimeChanged)
        self.dateTimeEdit.setCalendarPopup(True)
        self.guaM=MingGua(2000,1,1,0)
        self.ShowImg('bagua')
    def setupUI(self):
        loadUi('./ui/MingG_UI.ui',self)
    
    def to_main(self):
        sg=eight_gua2[self.guaM[0]]
        xg=eight_gua2[self.guaM[1]]
        temp=sg+xg
        print(sg)
        print(xg)
        print(temp)
        self.ShowImg(temp)

    def ShowImg(self,ImgName):
        self.m="./64_img/" +ImgName+".jpg"
        self.pm=QPixmap(self.m)
        self.imglabel.setPixmap(self.pm)
        self.imglabel.setScaledContents(True)

    def onDateTimeChanged(self,dateTime):
        a=str(dateTime)
        t=a[23:-1]
        dt=t.split(',')
        dt2=[int(x) for x in dt]
        self.guaM=MingGua(dt2[0],dt2[1],dt2[2],dt2[3])
        print(self.guaM)
if __name__ == '__main__':
    app=QApplication(sys.argv)
    mainwindow=QMainWindow()
    ui=mainWindow()
    ui.show()
    sys.exit(app.exec_())


