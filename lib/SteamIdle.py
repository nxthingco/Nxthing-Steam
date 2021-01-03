import re
import os
import time
from datetime import datetime
import steam
from steam.client import SteamClient
from steam.steamid import SteamID
from steam.enums import EResult
from steam.enums.emsg import EMsg
from steam.core.msg import GCMsgHdrProto
from steam.client.gc import GameCoordinator
import steam.webauth as sw
from ApiSteam import SteamApi

username = ''
password = ''

accs = []
cur_path = os.path.dirname(__file__)
new_path = cur_path + '/texts/accs_to_idle.txt'

with open (new_path,'r') as f:
	for i in f:
	    acc = i.replace(':',';').strip('\n').strip(' ').strip('\r').split(';')
	    acc = acc[0] + ';' + acc[1]
	    accs.append(acc)
	f.close()

"""

	Persona State = 
	Offline= 0
	Online= 1
	Busy= 2
	Away= 3
	Snooze= 4
	LookingToTrade= 5
	LookingToPlay= 6
	Invisible= 7
	Max= 8

"""

def StartIdle(client,PersonaState=1):
	print('---------------------')
	start = datetime.now()
	print('Start: ' + start.strftime("\nYear: %Y\nMonth: %B\nDay: %d\nTime: %H:%M:%S"))
	print('--------------------------------------')

	session = client.get_web_session_cookies()
	steam_id = session['steamLogin'][:17]
	try:
		Games = SteamApi.GetPlayerGames('FC50418A73E16C7AF179335DAC694619',steam_id)
		ProfilePrivate = False
	except:
		print('Error profile is private. Starting idling CS:GO,Dota 2')
		ProfilePrivate = True

	if ProfilePrivate != True:
		for x in Games:
			SteamApi.GetNameGameFromAppId(x)
		print('-----')
		print(Games[:32])
		print( 'Games: ' + ','.join(str(x) for x in Games))
	else:
		Games = [730,540]

	client.set_ui_mode(3)
	client.games_played(Games)
	client.change_status(persona_state=PersonaState)
	print('Games started.')
	print(client)
	while True:
		gamesnow = client.current_games_played
		if gamesnow:
			print(gamesnow)
			print('-------------')
			time.sleep(2)
		else:
			print('Буст прерван.')
			if client.relogin_available: client.relogin()
			print(gamesnow)
			client.games_played(Games)
			print(gamesnow)
			client.change_status(persona_state=2)

def idle(method,SAlogin=None,SApass=None):
	if method == 'MassAccount':
		print('Started Mass Account Idling...')
		clients = []
		users = []
		t = []
		for x in range(0,len(accs)):
			clients.append(x)
			users.append(x)

		for i in range(0,len(clients)):
			clients[i] = SteamClient() # КЛИЕНТЫ ГОТОВЫ
		for i in enumerate(accs):

			acc_id = i[0]
			acc = i[1].replace(':',';').strip('\n').strip(' ').strip('\r').split(';')

			username = acc[0]
			password = acc[1]

			r = clients[acc_id].login(username=username,password=password)
			if r == EResult.OK:
				print('Account Connected [{0}]: [{1}:{2}]'.format(acc_id,username,password))
				session = clients[acc_id].get_web_session_cookies()
				steam_id = session['steamLogin'][:17]
				try:
					Games = SteamApi.GetPlayerGames('FC50418A73E16C7AF179335DAC694619',steam_id)
					ProfilePrivate = False
				except:
					print('Error profile is private. Starting idling CS:GO,Dota 2')
					ProfilePrivate = True

				if ProfilePrivate != True:
					for x in Games:
						SteamApi.GetNameGameFromAppId(x)
					print('-----')
					print(Games[:32])
					print( 'Games: ' + ','.join(str(x) for x in Games))
				else:
					Games = [730,540]

				clients[acc_id].games_played(Games)
				clients[acc_id].change_status(persona_state=1)
				print('Games started.')
			else:
				print('Error: ' + str(r))
				continue

		while True:
			for z in range(0,len(accs)):
				gamesnow = clients[z].current_games_played
				if gamesnow:
					print(f'Account: {z}')
					print(gamesnow)
					print('-------------')
					time.sleep(2)
				else:
					print('Буст прерван.')
					if clients[z].relogin_available: clients[z].relogin()
					print(gamesnow)
					clients[z].games_played(Games)
					print(gamesnow)
					clients[z].change_status(persona_state=2)

	elif method == 'SingleAccount':
		
		#antenka33:vlodos33
		clientSA = SteamClient()
		login = clientSA.login(username=SAlogin,password=SApass)
		print(login)

		if login == EResult.OK:
			print('Account Connected: [{0}:{1}]'.format(SAlogin,SApass))
			StartIdle(clientSA)
		else:
			if login == EResult.LoggedInElsewhere: print('Steam Error: Logged In Elsewhere')

			elif login == EResult.NoConnection: print('No Connection')

			elif login == EResult.InvalidPassword: print('Invalid Password/Login')

			elif login == EResult.RateLimitExceeded: print('Steam Error: Try again later')

			elif login == EResult.AccountLoginDeniedThrottle: print('Login attempt failed, try to throttle response to possible attacker')

			elif login == EResult.AccountLogonDenied: 

				print('Account Login Denied')
				print('Trying login with email-code')
				code = input('Input Email-Code: ')

				login = clientSA.login(username=SAlogin, password=SApass, auth_code=code)

				if login == EResult.OK:
					print('Account Connected: [{0}:{1}]'.format(SAlogin,SApass))
					StartIdle(clientSA)
				else:
					print('Error: ' + login)


			elif login == EResult.AccountLoginDeniedNeedTwoFactor:
				code = input("Enter 2FA Code: ")
				login = clientSA.login(username=SAlogin, password=SApass, two_factor_code=code)

				if login == EResult.RateLimitExceeded:
					print('Steam Error: Try again later')

				elif login == EResult.AccountLoginDeniedThrottle:
					print('Login attempt failed, try to throttle response to possible attacker')

				elif login == EResult.TwoFactorCodeMismatch:
					print('Введен неверный 2FA Code, повторите попытку.')
					twofactor = input('Введите 2FA-Code: ')
					login = clientSA.login(username=SAlogin,password=SApass,two_factor_code=twofactor)

				if login == EResult.OK:
					print('Account Connected: [{0}:{1}]'.format(SAlogin,SApass))
					StartIdle(clientSA)
	else:
		print('[XSteam Error]: Wrong method selected.')