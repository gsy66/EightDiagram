import  sxtwl


Gan = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
Zhi = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
ShX = ["鼠", "牛", "虎", "兔", "龙", "蛇", "马", "羊", "猴", "鸡", "狗", "猪"]
numCn = ["零", "一", "二", "三", "四", "五", "六", "七", "八", "九", "十"]
jqmc = ["冬至", "小寒", "大寒", "立春", "雨水", "惊蛰", "春分", "清明", "谷雨", "立夏",
     "小满", "芒种", "夏至", "小暑", "大暑", "立秋", "处暑","白露", "秋分", "寒露", "霜降", 
     "立冬", "小雪", "大雪"]
ymc = ["十一", "十二", "正", "二", "三", "四", "五", "六", "七", "八", "九", "十" ]
rmc = ["初一", "初二", "初三", "初四", "初五", "初六", "初七", "初八", "初九", "初十", 
    "十一", "十二", "十三", "十四", "十五", "十六", "十七", "十八", "十九", "二十", 
    "廿一", "廿二", "廿三", "廿四", "廿五", "廿六", "廿七", "廿八", "廿九", "三十", "卅一"]
XiZ = ['摩羯', '水瓶', '双鱼', '白羊', '金牛', '双子', '巨蟹', '狮子', '处女', '天秤', '天蝎', '射手']
WeekCn = ["星期日", "星期一", "星期二", "星期三", "星期四", "星期五", "星期六"]

day=day = sxtwl.fromSolar(2023, 2, 25)
# 以春节为界的农历(注getLunarYear如果没有传参，或者传true，是以春节为界的)
s = "农历:%d年%s%d月%d日" % (day.getLunarYear(), 
    '闰' if day.isLunarLeap() else '', day.getLunarMonth(), day.getLunarDay())
#print(s)
s = "公历:%d年%d月%d日" % (day.getSolarYear(), day.getSolarMonth(), day.getSolarDay())
#print(s)
yTG = day.getYearGZ(True)
#print("以春节为界的年干支", Gan[yTG.tg] + Zhi[yTG.dz]) 
#print("以春节为界的生肖:", ShX[yTG.dz])
mTG = day.getMonthGZ()
#print("月干支", Gan[mTG.tg] + Zhi[mTG.dz]) 

#日干支
dTG  = day.getDayGZ()
#print("日干支", Gan[dTG.tg] + Zhi[dTG.dz]) 
#hour = 18
#sTG = day.getHourGZ(hour)
#print("%d时的干支"%(hour, ), Gan[sTG.tg] + Zhi[sTG.dz]) 



'''
年（属相来定数字）+月+日=上卦（留意：所得的和数除以8，余数就是上卦）
年（属相来定数字）+月+日+时辰（按照十二地支）=下卦（所得的和数除以8，余数就是下卦）
然后以年月日时的所得的和数除以6，余数就是动爻
最后是根据余数来对应八卦：乾卦是1，兑卦是2，离卦是3，震卦是4，巽卦是5，坎卦是6，艮卦是7，坤卦是8。
乾卦是1，兑卦是2，离卦是3，震卦是4，巽卦是5，坎卦是6，艮卦是7，坤卦是8
'''
g=['乾','兑','离','震','巽','坎','艮','坤']


def MingGua(year,month,daytime,hour):
    day = sxtwl.fromSolar(year, month, daytime)
    NumShang1=yTG.dz+1
    NumShang2=day.getLunarMonth()
    Numshang3=day.getLunarDay()
    Shanggua=(NumShang1+NumShang2+Numshang3)%8
    #print("{}:{}".format(ShX[yTG.dz],NumShang1))
    dizhi=[1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9, 10, 10, 11, 11, 12, 12, 1]
    xiagua=(Shanggua+dizhi[hour])%8
    dongyao=(Shanggua+dizhi[hour])%6
    #print("上卦{}，下卦{}".format(g[Shanggua],g[xiagua]))
    return [g[Shanggua],g[xiagua],dongyao]

