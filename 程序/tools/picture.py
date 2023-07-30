import requests
import re

url = "https://zhuanlan.zhihu.com/p/384810813"#需要爬取图片的网页地址
page = requests.get(url).text#得到网页源码
#print(page)
res = re.compile(r'data-actualsrc="(http.+?_b.jpg)"')#运用正则表达式过滤出图片路径地址
reg = re.findall(res, page)#匹配网页进行搜索出图片地址数组
#print(reg)

"""
<img src="https://pic3.zhimg.com/80/v2-9b2e11df6ebc3b4fb4e7cc590aeed12a_720w.webp" data-rawwidth="1080" data-rawheight="1080" data-size="normal" data-caption="" class="origin_image zh-lightbox-thumb lazy" width="1080" data-original="https://pic3.zhimg.com/v2-9b2e11df6ebc3b4fb4e7cc590aeed12a_r.jpg" data-actualsrc="https://pic3.zhimg.com/v2-9b2e11df6ebc3b4fb4e7cc590aeed12a_b.jpg" height="1080" data-lazy-status="ok">
"""

#循环遍历下载图片
num = 0
for i in reg:
    a = requests.get(i)
    f = open("64_img/%s.jpg"%(num+1), 'wb')#以二进制格式写入img文件夹中
    f.write(a.content)
    f.close()
    print("第%s张图片下载完毕"%(num+1))
    num = num+1
