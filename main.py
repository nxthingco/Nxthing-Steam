__version__ = '1.05'

import sys
sys.path.insert(0,'D:/XSteam/1/lib')
from SteamIdle import *
from GetSteamIDS import get_steam_info as GSI
from ParseSteamProfile import *
from SteamRetviver import *
from RegisterKeys import *
from GetSteamBackground import *

if __name__ == '__main__':
	print(Xtag + 'All loaded')
	"""if nSettings['RestartGames'] == True:
		print('Games will restart in 3 hours')
		while True:
			idle(nSettings['IdleMethod'])
			time.sleep(nSettings["RestartTime"])
	else:
		idle(nSettings['IdleMethod'])"""

#GetSteamBackGround('https://steamcommunity.com/profiles/76561198451887896')
#SteamRevive()
#idle('SingleAccount')