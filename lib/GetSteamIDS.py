from libs import *
class get_steam_info():
	def steamid(sid):
	    y = int(sid) - 76561197960265728
	    x = y % 2 
	    return "STEAM_0:{}:{}".format(x, (y - x) // 2)
	def steam32(sd):
		steamid3_r = sd.split(':')
		steamid_r = []
		steamid_r.append('[U:1:')
		y=int(steamid3_r[1])
		z=int(steamid3_r[2])
		steamacct = z * 2 + y
		steamid_r.append(str(steamacct) + ']')
		return ''.join(steamid_r)
	def steamid3(sd):
		steamid3_r = sd.split(':')
		steamid_r = []
		y=int(steamid3_r[1])
		z=int(steamid3_r[2])
		steamacct = z * 2 + y
		steamid_r.append(str(steamacct))
		return ''.join(steamid_r)
	def solo(text):
		r = SteamID.from_url(text)
		print('[1] - Steam 64: ' + str(r)) # 76561198044525640
		print('[2] - Steam ID: ' + get_steam_info.steamid(r)) # STEAM_0:0:42129956
		print('[3] - Steam 3 ID: ' + get_steam_info.steamid3(get_steam_info.steamid(r))) #U:1:84259912
		print('[4] - Steam 32 ID: ' + get_steam_info.steam32(get_steam_info.steamid(r))) #84259912
		print('[5] - Dotabuff: https://dotabuff.com/players/' + str(r))
	def mass(text):
		for url_1 in text:
			if url_1:	
				r = SteamID.from_url(url_1)
				print('[1] - Steam ID: ' + str(SteamID.from_url(url_1)))
				print('[2] - Steam64 ID: ' + get_steam_info.from64(r))
				print('[3] - Steam3 ID: ' + get_steam_info.steamid3(get_steam_info.steamid(r)))
				print('[4] - Steam 32 ID: ' + get_steam_info.steam32(get_steam_info.steamid(r)))
				print('Следующий аккаунт ...')
				print('\n')
			else:
				print('Ссылка на аккаунт не рабочая.')