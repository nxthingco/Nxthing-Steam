print('GetSteamBackground coming soon...')
from libs import *
from PIL import Image
from urllib.request import urlopen
#urlToMarket = 'http://steamcommunity.com/market/search?q=&category_753_Game[]=tag_app_{0}&category_753_item_class[]=tag_item_class_3&appid=753#p1_quantity_desc'.format()
AppIdForMarket = 0
def GetSteamBackGround(url):
	#if re.search('\S')
	request = requests.get(url)
	soup = BeautifulSoup(request.content,'html.parser')
	item = soup.find('div',class_='full_width_background')
	if item == None:
		print('Статичный фон не найден. Пробуем найти анимированный фон...')
		#animated = soup.find('div',class_='profile_animated_background')
		animated = soup.find('video')
		if animated:
			print('Найден анимированный фон.')
			animatelist = []
			for x in animated:
				animatelist.append(str(x))
			animated1 = re.split("'",''.join(animatelist))

			for x in ('source','autoplay','=','loop','muted','"','playsinline','poster','src',
						'>','<','\s+'):
				animated1 = re.split(x,''.join(animated1))
			del animated1[0],animated1[-1],animated1[-2]
			for x in animated1:
				if len(x) > 20:
					urlBackGround = x
				else:
					pass
			print(urlBackGround)
		else:
			print('На этом аккаунте нет фона.')
	else:
		item = item.get('style')
		#if item == None:
			#print('На аккаунте нет фона.')
		urlBackGround = ''

		item1 = re.split("'",''.join(item))
		for x in ('background-image','"','url',';','\s'):
			item1 = re.split(x,''.join(item1))
		for x in item1:
			if len(x) < 20:
				pass
			else:
				urlBackGround = x

		print(urlBackGround.split('/')[7])
def DownloadBackGroundOnPC():
	p = requests.get(urlBackGround)
	out = open("BackGroundImages\img.jpg", "wb")
	out.write(p.content)
	out.close()
	os.startfile(r'BackGroundImages\img.jpg')