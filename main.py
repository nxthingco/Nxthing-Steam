version = '1.12'

import sys
libpath = sys.path[0] + '\lib'
sys.path.insert(0,libpath)
from SteamIdle import *
from GetSteamIDS import get_steam_info as GSI
from new_ParseSteamProfile import *
from RegisterKeys import *
from ApiSteam import *
from update import *
from GUI import *

if __name__ == '__main__':
	print('All loaded')
	CheckVersion(version)
	OpenGui()