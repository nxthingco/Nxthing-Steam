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
import json

MAIN_API_KEY = '1'
MAIN_URL = 'https://steamcommunity.com/id/8k-'