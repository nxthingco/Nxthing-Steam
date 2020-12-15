import re
import os
import time
from datetime import datetime
from gevent import monkey
monkey.patch_all()
import requests
from bs4 import BeautifulSoup
import steam
import csgo
import steam.webauth as sw
from steam.client import SteamClient
from steam.steamid import SteamID
from steam.enums import EResult
from steam.enums.emsg import EMsg
from steam.core.msg import GCMsgHdrProto
from steam.client.gc import GameCoordinator
from csgo.enums import ECsgoGCMsg
from csgo.client import CSGOClient
from csgo.proto_enums import ECsgoSteamUserStat
import xmltodict
Xtag = '[XSteam]: '
Xtfa = '[XSteam 2FA Code Required] '
Xerror = '[ ! XSteam Error]: '
GamesToIdle = [629520,945360,550,12120,620,618140,206610,279720,303390,220,252150,
				253940,259340,500,10,444090,440,70,12110,240,230410,863550,238960,
				380,420,400,280]
GamesIdle = {
	'Counter-Strike: Global-Offensive': 730,
	'Dota 2':570,
	'Grimm': 252150,
	'Portal': '',
	'Half-Life 2': 220,
	'Left 4 Dead 2': 550,
	'Portal 2': 620,
	'3SwitcheD': 206610,
	'Among Us':945360,
	'Grand Theft Auto: San Andreas': 12120,
	'Barro':618140,
	'The I of the Dragon': 279720,
	'Soundpad': 629520,
	'Dead Bits': 303390,
	'HITMAN™ 2': 863550,
	'Counter-Strike':10,
	'Counter-Strike: Source':240,
	'Team Fortress 2':440,
	'Septerra Core': 259340,
	'Paladins':444090,
	"Grand Theft Auto: Vice City":12110,
	'Half-Life':70,
}
nSettings = {

	'RestartGames':True,
	'RestartTime':3600*3,
	'IdleMethod': 'SingleAccount',
	'SAlogin': 'UR_LOGIN',
	'SApass': 'UR_PASSWORD'
}