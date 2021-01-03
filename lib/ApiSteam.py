from gevent import monkey
monkey.patch_all()
import requests
from bs4 import BeautifulSoup
import json
import time
import re
from GetSteamIDS import get_steam_info as gsi

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

class SteamApi():

	def API_Get(method,url,apikey,steamid):
		if method == 1:
			session = requests.get(url + 'key=' + apikey + "&steamid=" + steamid)
			soup = BeautifulSoup(session.text,'html.parser')
			return soup
		elif method == 2:
			session = requests.get(url + 'key=' + apikey + "&steamid=" + steamid)
			return session.text
		elif method == 3:
			session = requests.get(url + 'key=' + apikey + "&steamids=" + steamid)
			soup = BeautifulSoup(session.text,'html.parser')
			return soup
		elif method == 4:
			session = requests.get(url + 'key=' + apikey + "&steamids=" + steamid)
			return session.text
		else:
			return '[API_Get]: Bad Method!'

	def GetPlayerGames(apikey,steamid):

		session = SteamApi.API_Get(2,PLAYER_OWNED_GAMES,apikey,steamid)
		r = json.loads(session)
		dr = r['response']['games']

		app_ids = []

		for i in range(0,len(dr)):
			dr = r['response']['games'][i]['appid']
			app_ids.append(dr)
		return app_ids

	def GetPlayerBadge(apikey,steamid):

		tagtostr = []

		session = SteamApi.API_Get(2,PLAYER_BADGE,apikey,steamid)
		r = json.loads(session)
		badge = len(r['response']['badges'])
		return badge

	def GetPlayerBans(apikey,steamids):
		r = SteamApi.API_Get(4,PLAYER_BANS,apikey,steamids)
		r = json.loads(r)
		SteamBansInfo = r['players'][0]
		CommunityBanned = str ( SteamBansInfo['CommunityBanned'] )
		VACBanned = str ( SteamBansInfo['VACBanned'] )
		NumberOfVACBans = str ( SteamBansInfo['NumberOfVACBans'] )
		DaysSinceLastBan = str ( SteamBansInfo['DaysSinceLastBan'] )
		GameBans = str ( SteamBansInfo['NumberOfGameBans'] )
		EconomyBan = str ( SteamBansInfo['EconomyBan'] )

		result = [CommunityBanned,VACBanned,NumberOfVACBans,DaysSinceLastBan,GameBans,EconomyBan]
		return result

	def GetSteamLevel(apikey,steamid):
		r = SteamApi.API_Get(2,PLAYER_LEVEL_STEAM,apikey,steamid)
		r = json.loads(r)
		level = r['response']['player_level']
		return level;

	def GetPlayerSummaries(apikey,steamids):
		dct = []

		session = SteamApi.API_Get(4,PLAYER_SUMMARIES,apikey,steamids)
		test = json.loads(session)
		SteamInfo = test['response']['players'][0]

		SteamId = str(SteamInfo['steamid'])
		Name = SteamInfo['personaname']
		RealName = SteamInfo['realname']
		Custom_URL = SteamInfo['profileurl']
		avatar = SteamInfo['avatarfull']
		Vanity_URL = 'https://steamcommunity.com/profiles/' + str(SteamInfo['steamid'])

		lastlogoff = time.localtime( int(SteamInfo['lastlogoff']) )
		lastlogoff = str(time.asctime(lastlogoff))

		CreatedDate = time.localtime( int(SteamInfo['timecreated']) )
		CreatedDate = str(time.asctime(CreatedDate))

		result = [SteamId,Name,RealName,Custom_URL,Vanity_URL,lastlogoff,CreatedDate,avatar]
		return result
	def GetNameGameFromAppId(app_id):
		response = requests.get('http://api.steampowered.com/ISteamApps/GetAppList/v0002/')
		data = json.loads(response.text)
		gameinfo = data['applist']['apps']
		for game in gameinfo:
			if game['appid'] == int(app_id):
				print(game['name'])

	def ShowAll(sapi,sid):
		print(SteamApi.GetPlayerSummaries(sapi,sid))
		print('Level: ' + str( SteamApi.GetSteamLevel(sapi,sid) ))
		print(SteamApi.GetPlayerBans(sapi,sid))
		print('Badges: ' + str( SteamApi.GetPlayerBadge(sapi,sid) ))