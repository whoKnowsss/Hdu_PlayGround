#  coding:utf-8 
##  先安装环境python3、pip环境
##  pip3 install requests
##  pip3 install BeautifulSoup4
##  sudo apt-get install python3-lxml 或者 pip3 install lxml
##  顶点小说爬虫
##  输入小说的网址进行下载
##  example： https://www.booktxt.net/8_8937/
##  直接运行即可  python3 dingdian_novel_download.py
##  测试环境为win10-python3
##  author: lxfhahaha
##  date: 2018年5月27日13:59:21

import	requests
from bs4 import BeautifulSoup
import re
import sys,io
from multiprocessing.dummy import Pool as threadpool

class Novel(object):              ## 小说类
	title=''			## 小说名字
	author=''			## 小说作者
	content=[]			## 小说内容 （序号，标题，内容/url）
	url=''  			## 小说网址
	
	def set_url(self,headers):    ## 设置网址
		url=''
		while True:
			url=input('Your url:')
			if(url.startswith('https://www.booktxt.net/')):
				r1=requests.get(url,headers=headers)
				if r1.status_code==200:
					break
			print('Error!Input again~')
			sys.stdout.flush()
		self.url=url


	def add_section(self,num,titleThis,content):      ##加章节
		self.content.append([num,titleThis,content])


	def get_details(self,headers):  				  ##获得具体信息，包括小说名字、作者、各章节url,返回一个Novel对象
		req=requests.get(self.url,headers=headers)
		so1=BeautifulSoup(req.content.decode('gbk'),'lxml')
		self.title=so1.select('#maininfo #info h1')[0].get_text()  ##小说名字
		self.author=so1.select('#maininfo #info p')[0].get_text()  ##作者名字

		startTag=so1.select('#list dl dt')[1]				  ##设置各章节名称、序号、url
		for index,one in enumerate(startTag.find_all_next("dd")):
			self.add_section(num=index+1,titleThis=one.a.get_text(),content='https://www.booktxt.net'+one.find('a').get('href'))

	



	def get_content_all(self,headers):    ## 爬虫爬取各章节内容，单线程

		def make_great(one):
			r2=requests.get(one[2])
			if r2.status_code==200:
				so2=BeautifulSoup(r2.content.decode('gbk'),'lxml')
				one[2]=so2.select('#content')[0].get_text()
			else:
				one[2]='内容错误！'
			self.allLength=self.allLength-1
			print (str(one[0])+' is ok! '+str(self.allLength)+' left!')
			sys.stdout.flush()
			return one
		
		self.allLength=len(self.content)
		print('all is '+str(self.allLength))
		sys.stdout.flush()
		
		self.content=[make_great(one) for one in self.content]



	def get_content_all_pool(self,headers):    ## 爬虫爬取各章节内容，多线程
		
		self.allLength=len(self.content)
		print('all is '+str(self.allLength))
		sys.stdout.flush()

		def getAll(one):
			r2=requests.get(one[2])
			if r2.status_code==200:
				so2=BeautifulSoup(r2.content.decode('gbk'),'lxml')
				one[2]=so2.select('#content')[0].get_text()
			else:
				one[2]='内容错误！'
			self.allLength=self.allLength-1
			print (str(one[0])+' is ok! '+str(self.allLength)+' left!')
			sys.stdout.flush()
			return one

		
		pool=threadpool(4)
		result=pool.map(getAll,self.content)
		pool.close()
		pool.join()
		self.content=result


	def downloadToTxt(self):
		file=open(self.title+'.txt','w+',encoding='utf-8')
		file.write('*****'+self.title+'-'+self.author+'*****\n\n\n')
		self.content.sort(key=lambda x:x[0])   		  ##对第一个关键字进行排序，使内容有序
		for one in self.content:	
			file.write('### '+one[1]+'\n\n')
			file.writelines(one[2]+'\n\n')
		file.close()	
		print('End Downloads and start enjoying!!')	
		sys.stdout.flush()





if __name__ == '__main__':          ##主函数入口
	
	#改变标准输出的默认编码
	sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gbk') 
	
	#头信息，有利脚本稳定
	headers={
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
		'Referer':'https://www.booktxt.net/'
		}
	

	#新建novel对象
	novel=Novel()


	#确认小说网址
	novel.set_url(headers=headers)


	#获得具体信息（书名，作者，各章节url）
	novel.get_details(headers=headers)


	#获得所有章节内容
	#可选，单线程或者多线程

	danDuo=input('Y/n to choose whether use multithreading:')
	if (danDuo=='Y' or  danDuo=='y'):
		novel.get_content_all_pool(headers=headers)  	#多线程
	else:
		novel.get_content_all(headers=headers)   		#单线程
	
	


	#下载小说
	novel.downloadToTxt()

