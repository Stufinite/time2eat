#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests, json, pyprind, sys, shutil, re, pickle
from bs4 import BeautifulSoup

def startCrawler(fileName):

	res = requests.get('http://www.gomaji.com/index.php?city=Taichung')
	#一開始的台中頁面  然後去爬上面所有的餐廳分類網址
	soup = BeautifulSoup(res.text)

	location = soup.select('.sf-with-ul')[0].text #得到縣市的文字  這邊是台中
	global json_arr # global var : 最終結果json，在python中，想要再函式裏面呼叫全物變數要加一個global
	json_arr = {location:{}}

	aLen = len(soup.select("#lb_tag  a"))/2 # "lb_tag  a"是餐廳分類的tag 但是每個分類都有2個重複的tag，所以要/2
	aIndex = 1
	ProgreBar = pyprind.ProgBar(aLen, title = "{} 共 {} 個餐廳類別要處理" .format( location, aLen)) #建立一個進度條物件

	for a in soup.select("#lb_tag  a"):
		# soup.select("#lb_tag  a") 會選取到餐廳分類的超連結 <a>這的tag然後把他的網址抓出來，進到那個分類 例如火鍋，再把所有火鍋類的餐廳爬出來
		href = a['href']
		resType = a.text #餐廳類別的中文字  例如火鍋
		if aIndex > aLen: break
		aIndex = aIndex + 1
		parsePage(base_url+href, location, resType) # 把火鍋的網址傳進函式裏面然後開始爬火鍋那一類別的所有資料
		ProgreBar.update(1,item_id = aIndex, force_flush=True)#item_id可以讓使用者追蹤到底執行到第幾個ID
		#ID通常是放for loop裏面的變數，update()會讓進度條更新

	dump(fileName) #儲存json
	dumpResTable(ResTable)

def parsePage(url, location, resType):
	res = requests.get(url)
	childSoup = BeautifulSoup(res.text)
	tmp = {resType:[]}

	for i, img in zip(childSoup.select('ul.deal16 li.box-shadow2px'), childSoup.select('ul.deal16 li.box-shadow2px img')):
		href = i.find('a')['href']# 把a的href屬性的值抓出來
		href = base_url+href
		d = getResProf(href) # getResPro這個函式會進入到某一間餐廳的簡介，簡介寫的資料比較完整，但是格式並沒有固定，出錯機率極高

		restaurant = i.find('a').find('div','boxc').find('h2')# find可以找到他的child那一層
		restaurant = purgeResName(restaurant.text.strip(), d)

		if restaurant not in ResTable:
			# 更新餐廳名稱的set
			ResTable.add(restaurant)
			savePict(img, restaurant)
			d["url"] = href
			d['restaurant'] = restaurant
			tmp[resType].append(d)

	json_arr[location].update(tmp)

def dumpResTable(ResTable):
	pickle.dump(ResTable, open("ResTable.pickle", "wb"))

def dump(fileName):
	with open(fileName, 'w', encoding='UTF-8') as f:
		json.dump(json_arr, f)

def purgeResName(raw, d):
	# if dictionary didn't have 'restaurant' this key, means getResProf throw an exceptions while running, so we need to find the restaurant name by other means which is not our priority ( code in except clause is an alternative method )
	try:
		return d['restaurant']
	except Exception as e:
		raw = raw.replace('/','')
		return raw.split('】')[0].replace('【','')

def getResProf(href):
	res = requests.get(href)
	resSoup = BeautifulSoup(res.text)
	tmp = {}
	num=1
	# 去爬餐廳簡介的資料，因為格式沒有完全統一，所以需要很多try catch防止程式噴錯
	try:
		for i in resSoup.findAll('div', style="display: table-cell;")[1].children:
			try:
				if len(i.text) > 0:     
					# 因為第一個都是餐廳名稱（理論上），所以需要一個num來紀錄現在是for回圈的第幾次
					if num==1:
						tmp['restaurant'] = i.text.replace('/','')
					else:     
						i = re.sub(r'(\r)*(\t)*(\n)*','',i.text)
						clean = i.split('：')
						tmp[clean[0]] = clean[1]
					num=num+1
			except AttributeError as e:
				pass
	except Exception as e:
		err_url.append(href)
	return tmp

def savePict(img, restaurant):
	imageUrl = img['src']
	img = requests.get(imageUrl,stream=True)
	with open(restaurant+'.jpg', 'wb') as f:
		shutil.copyfileobj(img.raw, f)

def saveERR():
	with open('err_url.json', 'w', encoding='UTF-8') as e:
		json.dump(err_url, e)

if __name__  ==  "__main__":
	if len(sys.argv) < 2:
		#sys.argv[0]是模組名稱喔!
		print("Usage:\n\tpython[3] "+sys.argv[0]+" <filename.json>")
		print("\n\tURL can be:http://www.gomaji.com/index.php?city=Taichung&tag_id=99");
		sys.exit(1)#0為正常結束，其他數字exit會拋出一個例外，可以被捕獲

	base_url = "http://www.gomaji.com/"
	err_url = []
	json_arr = {} # 最終結果json
	ResTable = set() # 建立餐廳名稱的set
	# 而在函式裏面，如果你有指派值給該變數，python就會自動為你建立區域變數
	ResTable = pickle.load(open("ResTable.pickle", "rb"))
	startCrawler(sys.argv[1])
	saveERR() # 把發生錯誤的網址處存起來
