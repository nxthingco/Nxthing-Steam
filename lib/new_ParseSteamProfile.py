from libs import *
from ApiSteam import *
from GetSteamIDS import get_steam_info as gsi

def InventoryItems(url):
	session_z = requests.get(url + '/inventory')
	soup_z = BeautifulSoup(session_z.content,'html5lib')
	inventorycheck = soup_z.find_all('span','games_list_tab_name')
	countInventoryItems = soup_z.find_all('span','games_list_tab_number')
	par = []
	cII = []
	for x in countInventoryItems:
		cII.append(str(x))
	cII4 = re.split('class',''.join(cII)) # <--------- РАБОТАЕТ ТОЛЬКО С ЭТОЙ СТРОКОЙ
	for x in ('[(< >)/="]','games_list_tab_number','span'):
		cII4 = re.split(x,''.join(cII4))
	for x in inventorycheck:
		par.append(str(x))
	test4 = re.split('class',''.join(par))
	for x in ('[<>/="]','games_list_tab_name','span'):
		test4 = re.split(x,''.join(test4))
	del cII4[0]
	del test4[0]
	# Создание кортежа из 2 списков(одинаковой длины)
	items_and_count = dict(zip(test4,cII4))
	for k,v in items_and_count.items():
		print('[Game: {0}] - [Items: {1}]'.format(k,v))

def ParseSteamProfile(apikey,url):

	steam_id = str ( gsi.SteamId(url) )
	PlayerInfo = SteamApi.GetPlayerSummaries(apikey,steam_id)
	PlayerBans = SteamApi.GetPlayerBans(apikey,steam_id)

	print(	'Name: ' + PlayerInfo[1] + '\n' +
			'RealName: ' + PlayerInfo[2] + '\n' +
			'Custom_URL: ' + PlayerInfo[3] + '\n' +
			'Vanity_URL: ' + PlayerInfo[4] + '\n' +
			'Last Logoff: ' + PlayerInfo[5] + '\n' +
			'Since Date: ' + PlayerInfo[6] + '\n' + 
			'Steam ID 64:' + PlayerInfo[0] + '\n')

	print('Level: ' + str( SteamApi.GetSteamLevel(apikey,steam_id) ))
	print('Badges: ' + str( SteamApi.GetPlayerBadge(apikey,steam_id) ))

	print(	'Community Banned: ' + PlayerBans[0] + '\n' +
			'VAC Banned: ' + PlayerBans[1] + '\n' +
			'Number Of VAC Bans: ' + PlayerBans[2] + '\n' +
			'Days Since Last Ban: ' + PlayerBans[3] + '\n' +
			'Game Bans: ' + PlayerBans[4] + '\n' +
			'Economy Ban: ' + PlayerBans[5] + '\n')

	try:
		gsi.solo(url)
	except:
		print('Не удалось вычислить Steam IDS')
	try:
		InventoryItems(url)
	except:
		print('Не удалось загрузить информацию о инвенторе')