from libs import *

url = 'https://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v2/'
FRIEND_LIST = 'https://api.steampowered.com/ISteamUser/GetFriendList/v1/?'
PLAYER_SUMMARIES = 'https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/?'
RESOLVE_VANITY_URL = 'https://api.steampowered.com/ISteamUser/ResolveVanityURL/v1/?'
PLAYER_BANS = 'https://api.steampowered.com/ISteamUser/GetPlayerBans/v1/?'
PLAYER_GAMES = 'https://partner.steam-api.com/ISteamUser/GetPublisherAppOwnership/v3/?'
PLAYER_BADGE = 'https://api.steampowered.com/IPlayerService/GetBadges/v1/?'
PLAYER_OWNED_GAMES = 'https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/?'
PLAYER_OWNED_GAMES_F = 'https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/?&include_played_free_games=1&include_free_sub=1'
PLAYER_LEVEL_STEAM = 'https://api.steampowered.com/IPlayerService/GetSteamLevel/v1/?'


FRIENDS_COUNT = 0

INCLUDE_APPINFO = 0
INCLUDE_PLAYED_FREE_GAMES = 0
INCLUDE_FREE_SUB = 1

# getting app ids
def GetPlayerGames():
	#url = 'https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/?&key=FC50418A73E16C7AF179335DAC694619&include_played_free_games=1&include_free_sub=1&steamid=76561198044525640'
	url = PLAYER_OWNED_GAMES + '&key=' + api_key + '&' + steam_id
	session = requests.get(url)
	r = json.loads(session.text)
	dr = r['response']['games']

	app_ids = []

	for i in range(0,len(dr)):
		dr = r['response']['games'][i]['appid']
		app_ids.append(dr)
	print(app_ids)

def API_SteamCheck(method,url,apikey,steamId):
	if method == 1:
		session = requests.get(url + 'key=' + apikey + "&" + steamId)
		soup = BeautifulSoup(session.text,'html.parser')
		return soup
	elif method == 2:
		session = requests.get(url + 'key=' + apikey + "&" + steamId)
		return session.text
	else:
		return '[API_SteamCheck]: Bad Method!'


def GetFriendsCount(apikey,steamid):
	soup = API_SteamCheck(1,FRIEND_LIST,apikey,steamid)
	relation = re.findall('relationship',''.join(soup))
	for i in range(0,len(relation)):
		FRIENDS_COUNT = i+1
	return FRIENDS_COUNT;
	#print('Friends Count: ' + str(FRIENDS_COUNT))

def GetPlayerBadge(apikey,steamid):
	soup = API_SteamCheck(1,PLAYER_BADGE,apikey,steamid)
	print(soup)
	badge = re.findall('badgeid',''.join(soup))
	print(badge)
	for i in range(0,len(badge)):
		badge = i+1
	return badge

def GetPlayerBans(apikey,steamids):
	r = API_SteamCheck(2,apikey,api_key,steamids)
	r = json.loads(r)

	SteamBansInfo = r['players'][0]

	print('Community Banned: ' + str( SteamBansInfo['CommunityBanned'] ) ) 
	
	if SteamBansInfo['VACBanned']:
		print('VAC Banned: ' + str( SteamBansInfo['VACBanned'] ) + '(' + str( SteamBansInfo['NumberOfVACBans'] ) + ')')
		print('Days Since Last Ban: ' + str(SteamBansInfo['DaysSinceLastBan']) )
	else:
		print('VAC Banned: ' + str(SteamBansInfo['VACBanned']) )

	print('Game Bans: ' + str(SteamBansInfo['NumberOfGameBans']) )

	print('Economy Banned: ' + str(SteamBansInfo['EconomyBan']) )

def GetSteamLevel(apikey,steamid):
	r = API_SteamCheck(2,PLAYER_LEVEL_STEAM,apikey,steamid)
	r = json.loads(r)
	level = r['response']['player_level']
	return level;

def GetPlayerSummaries(apikey,steamids):
	dct = []

	session = API_SteamCheck(2,PLAYER_SUMMARIES,apikey,steamids)
	test = json.loads(session)
	SteamInfo = test['response']['players'][0]


	lastlogoff = time.localtime( int(SteamInfo['lastlogoff']) )
	lastlogoff = time.asctime(lastlogoff)


	CreatedDate = time.localtime( int(SteamInfo['timecreated']) )
	CreatedDate = time.asctime(CreatedDate)


	#print(test)

	print('SteamID: ' + str(SteamInfo['steamid']))
	print('Name: ' + SteamInfo['personaname'])
	print('Настоящее имя: ' + SteamInfo['realname'])
	print('Custom URL: ' + SteamInfo['profileurl'])
	print('Vanity URL: https://steamcommunity.com/profiles/' + str(SteamInfo['steamid']))
	print('Дата создания аккаунта: ' + str(CreatedDate))
	print('Последний выход: ' + str(lastlogoff))
	try:
		print('Значков у игрока: ' + str(GetPlayerBadge(apikey,SteamInfo['steamid'])))
	except:
		print('Не удалось загрузить страницу с информацией о значках')
	try:
		print('Уровень STEAM: ' + str( GetSteamLevel(apikey,SteamInfo['steamid']) ))
	except:
		print('Не удалось загрузить страницу с информацией о уровне')
	print('----------------------------------------------------')
	try:
		print( GetFriendsCount(apikey,SteamInfo['steamid']) )
	except:
		print('Не удалось загрузить страницу с информацией о друзьях')
	try:
		GetPlayerBans(apikey,SteamInfo['steamid'])
	except:
		print('Не удалось загрузить страницу с информацией о банах')