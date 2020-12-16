from libs import *
from GetSteamIDS import get_steam_info as GSI
url = ''
def GetGamesInDict(steamid):
    headers = {'User-Agent':"Mozilla/5.0 (Linux; Android 8.0.0; SM-G960F Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.84 Mobile Safari/537.36","content-type": "application/json","Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9","Accept-language":"en-US,en;q=0.5"}
    r = requests.get(f"https://steamcommunity.com/profiles/{steamid}/games/?tab=all&xml=1",headers = headers).text
    z = xmltodict.parse(r)
    return z
def parse_steamprofile():
	d = input('[XSteam] Введите URL/Steam ID: ')
	if re.search('[A-Za-z]',d) == None:
		if len(d) == 17:
			if re.search('[.,;:[]/?<>]',d):
				print('Найдены лишние символы')
		print('Преобразовываем STEAM ID 64 В ссылку')
		url = 'https://steamcommunity.com/profiles/' + d
	elif re.search('[A-Za-z]',d):
		GSI.solo(d)
		url = d
	else:
		print('[XSteam Error]: Bad URL/Steam ID')
	session = requests.get(url)
	session_z = requests.get(url + '/inventory')
	session_games = requests.get(url + '/games/?tab=all&xml=1')
	badge_response = requests.get(url + '/badges/1')

	soup_x = BeautifulSoup(session.content,'html5lib')
	soup_z = BeautifulSoup(session_z.content,'html5lib')
	soup_c = BeautifulSoup(session.text,'html5lib')
	soup_games = BeautifulSoup(session_games.text,'html5lib')
	soup_badge = BeautifulSoup(badge_response.text,'html.parser')
	########################### INVENTORY PARSE (NEED REWORK)######################
	inventorycheck = soup_z.find_all('span','games_list_tab_name')
	countInventoryItems = soup_z.find_all('span','games_list_tab_number')
	vanityurl = soup_c.find(string=re.compile('g_rgProfileData'))
	r_games = soup_games.find_all('name')
	# КОЛ-ВО ПРЕДМЕТОВ ИНВЕНТАРЬ
	# Конвертирование тэга в list
	par = []
	cII = []
	for x in countInventoryItems:
		cII.append(str(x))
	cII4 = re.split('class',''.join(cII)) # <--------- РАБОТАЕТ ТОЛЬКО С ЭТОЙ СТРОКОЙ
	for x in ('[(< >)/="]','games_list_tab_number','span'):
		cII4 = re.split(x,''.join(cII4))
	for x in inventorycheck:
		par.append(str(x))
	test4 = re.split('class',''.join(par)) # <--------- РАБОТАЕТ ТОЛЬКО С ЭТОЙ СТРОКОЙ
	for x in ('[<>/="]','games_list_tab_name','span'):
		test4 = re.split(x,''.join(test4))
	# Создание кортежа из 2 списков(одинаковой длины)
	del test4[0]
	del cII4[0]
	items_and_count = dict(zip(test4,cII4))
	# КОЛИЧЕСТВО ИГР
	info = GetGamesInDict(SteamID.from_url(url))
	GamesCount = len(info["gamesList"]["games"]["game"])
	#ДАТА СОЗДАНИЯ АККАУНТА
	MemberSince = soup_badge.find('div',class_='badge_description')
	#################################################################################
	try:
		name = soup_x.find('span','actual_persona_name').text
		level = soup_x.find('span','friendPlayerLevelNum').text
		country = soup_x.find('div','header_real_name').text
		d = re.search(' ᠌᠌',country)
		if d == " " or ' ᠌᠌':
			country = '\n'
		real_name = soup_x.find('bdi','').text
		e = re.search(' ᠌᠌',real_name)
		if e == " " or ' ᠌᠌':
			e = '\n'
		print('Nick: ' + name + '\n'
			+ 'Level: ' + level + '\n' 
			+ 'Country: ' + country.rstrip('\n')
			+ 'Real Name: ' + real_name + '\n')
		#test_f = re.split('\s+',''.join(test18))
	except:
		print('Закрытый профиль')
	try:
		ban = soup_x.find('div','profile_ban_status').text
		d = re.findall('VAC',ban)

		if d[0] == 'VAC':
			print('На Аккаунте имеется блокировка VAC')
	except:
		print('VAC не найден')
	private_profile = soup_x.find('div','profile_private_info')

	if MemberSince:
		MemberSince = re.split('\s+',''.join(MemberSince))
		del MemberSince[0],MemberSince[-1]
		print(''.join(MemberSince))
	else:
		print('Невозможно определить дату создания аккаунта')

	# Конвертирование тэга в list
	qw = []
	for x in r_games:
		qw.append(str(x))
	w = ''.join(qw)
	
	test = soup_x.select('.profile_in_game_header')
	test2 = soup_x.select('.profile_in_game_name')
	StageCur = []
	for x in test:
		StageCur.append(str(x))
	StageCurr = [6]
	StageCurr1 = re.split('div',''.join(StageCur))
	for x in ('div','class','[<>=/"]','profile_in_game_header','\s'):
		StageCurr1 = re.split(x,''.join(StageCurr1))

	if private_profile == None:
		print('Профиль открыт')
	else:
		print('Профиль закрыт')
	print('Игр на аккаунте: ' + str(GamesCount))
	print('Состояние:{0}'.format(' '.join(StageCurr1)))
	print('------------------------ [Steam IDS] ------------------------')
	GSI.solo(url)
	print('Permalink: https://steamcommunity.com/profile/' + str(SteamID.from_url(url)))
	#print('Profile URL: ' + ':'.join(vanityurl18))
	print('------------------------ [Inventory] ------------------------')
	print('\n')
	for k,v in items_and_count.items():
		print('[Game: {0}] - [Items: {1}]'.format(k,v))
	for i in ('/','<','>','name',']','[','--','','CDATA'):
		w = w.replace(i,'')
	print('------------------------ [Games] ------------------------')
	out = w.split('!')
	del out[0]
	for k in out:
		print('[Game: {0}]'.format(k))
	#print('Games: ' +'\n '.join(out))