基于pyqt5的赛博算卦软件
=======================
[toc]
# 1.使用介绍
&emsp;&emsp;这是一款基于pyqt5库编写的赛博算卦软件，具有一键成卦和自行解卦等功能。作者由于心血来潮，同时也为了学习一定的pyqt5相关代码的编写方式，编写了这个小软件。同时也练习了python爬虫爬取相关网站的信息的方法。其中包含一键成卦、手动算卦、命卦计算等方式，并根据一定算法形成卦爻辞。
&emsp;&emsp;具体工程文档链接上传到两处：
CSDN资源库：[https://download.csdn.net/download/gsy_nb/88180522](https://download.csdn.net/download/gsy_nb/88180522)（更新可能不够频繁）
Github：[https://github.com/gsy66/EightDiagram](https://github.com/gsy66/EightDiagram)(基本同步更新)

# 2.资料准备与爬取
## 2.1文字信息爬取
&emsp;&emsp;在有这个想法的时候，我便开始去网上搜索一些图片。文字等的资料。很幸运的是，在简单的搜索后，我在某乎发现了一篇文章[(链接)](https://zhuanlan.zhihu.com/p/377091070)，包含着每一卦的卦辞和爻词。便利用python的BeautifulSoup库等对相关信息进行爬取（具体使用方法可以参考其他博主文章），并进行分类整合。
&emsp;&emsp;将所得到的数据以类似的字典格式存放，为了便捷之后的软件对数据进行调用，也为了方便自己以后代码编写思路的清晰。
具体代码以下为例:
```python
from bs4 import BeautifulSoup
import requests
import re
#从知乎上爬取卦爻辞并整理
url="https://zhuanlan.zhihu.com/p/377091070"

r =  requests.get(url,timeout=30)
r.encoding = r.apparent_encoding      
#分析页面内容，以中文编码显示
html = r.text
soup = BeautifulSoup(html, 'html.parser') 
 

#访问head、body、a、p、b
def guaming_get():
    h1 = soup.select('h2')
    f = open('./text/guaming.txt',"w",encoding='utf-8')
    print(type(h1))
    h2 = h1[0].text
    for h in h1:
        print(h.text)
        h2 = re.findall(r".上.*?下",h.text)
        h3 = re.findall(r' .*? .*? .上.*?下',h.text)
        print(h2)
        print(h3)
        if h2 !=[] and h3!=[]:
            f.write("{}:{}\n".format(h2[0],h3[0]))
        elif h2 !=[] and h3 ==[]:
            f.write("{}:\n".format(h2[0])) 
    f.close()
def guaci_get():
    a=soup.select('p')
   # print(a)
    t=[]
    for h in a:
        #print(h.text)
        h3=re.findall(r'[\u4e00-\u9fa5]+：.*?。',h.text)
        h4=re.findall(r'《[\u4e00-\u9fa5]》曰：.*?',h.text)
        if (h3!=[] and re.findall(r'曰',h3[0])==[]):
           # print(h.text)
            temp=[]
            temp1=h.text.strip().split("：")
            temp.append(temp1[0])
            temp.append(temp1[1])
            flag=0
        #if(h3 !=[]):
        if (h4!=[] and re.findall(r'《[\u4e00-\u9fa5]》曰',h4[0]) !=[]):
            if flag==0:
                temp.append(h.text.strip())
                flag=1
            elif flag==1:
                temp.append(h.text.strip())
                t.append(temp)
    return t
       
def yaoci_get():
    t=[]
    h1=soup.select('tbody')
    for h in h1:
        h2 = h.select('tr')
        tempm=[]
        for x in h2:
            x2=x.select('td')
            n=0
            tempn=[]
            for x3 in x2:
                if n==0:
                    temp1=x3.text
                    tempn.append(temp1[0]+temp1[1])
                    tempn.append(temp1)
                    n+=1
                else:
                    tempn.append(x3.text)
            tempm.append(tempn)
        t.append(tempm)
        #print(tempm)
    return t


f=open("./text/guaci_yaoci.txt","w",encoding='utf-8')
"""
{
    "乾":{
        "卦":['乾：元，亨，利，贞。','《彖》曰：', '《象》曰：'],
        "爻":[[1,2],[1,3],[1,4],[1,5],[1,6],[1,7]]
    }
}
"""
a=guaci_get()
b=yaoci_get()
#f.write('{')
dicta={}
for i in range(len(a)):
    guaming=a[i][0]+"卦"
    guaci=a[i][1]
    guayuan=a[i][2]
    guaxiang=a[i][3]
    yaoci =b[i] 
    dicta[guaming]={
        "卦":[guaci,guayuan, guaxiang],
        "爻":[yaoci[0],yaoci[1],yaoci[2],yaoci[3],yaoci[4],yaoci[5]]
    }
f.write(str(dicta))
#f.write("}")
f.close()
```
## 2.2图片信息整理与爬取
&emsp;&emsp;在整理图片信息的时，由于算卦方式及卦本身的特点，用0表示阴爻，用1表示阳爻，从上至下依次表示六根爻，就能够很好的检索到对应卦象所对应的图片。但是后来在编写程序的时候，发现这种从上到下命名名称的方式其实并不好，因为算卦相关的算法一般来说都是至下而上的，导致后面每次需要检索的时候都要进行一个倒置，也就多了一点麻烦，但是由于本人较懒，就没改（也许这就是屎山形成的原因）。
具体图片及代码在整个文档的64_img文件夹里。
*****************
# 3.ui设计
ui设计采用designer设计。
# 4.算法参考
# 5.图片显示及交互按钮