import requests
from lxml import etree
import re
import os
import time
#得到每一个图集url+title
def getmmpics(url):
	header={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36"}
	time.sleep(1)
	r=requests.get(url,headers=header)
	#编码gb18030
	r=r.content.decode('gb18030')
	#print(r.status_code)
	html=etree.HTML(r)
	mmpicsurl=html.xpath('//div[@class="MeinvTuPianBox"]/ul/li/a[@class="MMPic"]/@href')
	mmpicstitle=html.xpath('//div[@class="MeinvTuPianBox"]/ul/li/a[@class="MMPic"]/@title')
	return mmpicsurl,mmpicstitle

#得到每张图片url
def getpicurl(urls,titles,everydir):
	titles=titles.replace("'","")
	header={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36"}
	if everydir:
		path='./'+titles+'/'
		#判断文件夹是否存在
		if os.path.exists(path):
			pass
		else:
			os.mkdir(path)
	else:
		path="./"
	#获取每张图片链接
	for i in range(10):
		temp=f"_{i+1}.html"
		url=re.sub(".html",temp,urls)
		time.sleep(1)
		r=requests.get(url,headers=header)
		html=etree.HTML(r.text)
		src=html.xpath('//p[@align="center"]/a/img/@src')
		src = ''.join(src)
		#src=src.strip("'")
		src=src.replace("'","")
		#照片name
		name=src.split('/')
		name=name[len(name)-1]
		if everydir:
			pass
		else:
			name=titles+name
		#判断是否存在这张照片
		photopath=path+name
		#print(photopath)
		if os.path.exists(photopath):
			print("第%d张图片已存在"%(i+1))
			continue
		else:
			print("正在下载第%d张图片"%(i+1))
			savepic(src,path,name)

#保存每一张图片
def savepic(src,path,name):
	#print(src)
	header={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36"}
	time.sleep(1)
	data=requests.get(src,headers=header)
	if data.status_code==200:
		#print(name)
		#写入文件
		with open(path + name,"wb") as f:
			f.write(data.content)
	else:
		print("第%d张图片不存在"%(i+1))
		return

if __name__=="__main__":
	#1-253=253页 (253*30-1)*10=75890
	#count=input("输入要下载的页面数(1~253)：")
	print("抓取图片，共253页，每页30套")
	print("eg.页码为[5,5]则下载第5页;页码为[2:20]下载2~20页")
	kaishi=int(input("输入开始页数："))
	jieshu=int(input("输入结束页数："))
	everydir=int(input("是否为每套图分别存放文件夹？(输入1分别存放/0放在一起)："))
	url0="https://www.2717.com/ent/meinvtupian/"
	#每一页
	for i in range(kaishi,jieshu+1):
		print("开始下载第%d页"%i)
		temp=f"list_11_{i}.html"
		url=url0+temp
		#一页上的urls，titles
		mmpicsurl,mmpicstitle=getmmpics(url)
		mmpics=1
		for urls,titles in zip(mmpicsurl,mmpicstitle):
			urls="https://www.2717.com"+urls
			#print(titles)
			print("正在下载第%d页的第%d套"%(i,mmpics))
			getpicurl(urls,titles,everydir)
			mmpics=mmpics+1

