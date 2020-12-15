from libs import *

def idle(method):
	if method == 'MassAccount':
		clients = []
		users = []
		t = []
		for x in range(0,len(tAccounts)):
			clients.append(x)
			users.append(x)
		for i in range(len(clients)):
			clients[i] = SteamClient()
		for z in range(0,len(tAccounts)):
			r = clients[z].login(username=tAccounts[z],password=tPasswords[z])
			if r == 'EResult.OK':
				print(Xtag + 'Account Connected [{1}]: [{2}:{3}]'.format(i,tAccounts[z],tPasswords[z]))
			else:
				print(Xerror + str(r))
				continue
			clients[z].set_ui_mode(2)
			clients[z].games_played(GamesToIdle)
			start = datetime.now()
			print('Start: ' + start.strftime("\nYear: %Y\nMonth: %B\nDay: %d\nTime: %H:%M:%S"))
		for z in range(0,len(tAccounts)):
			clients[z].run_forever()
	elif method == 'SingleAccount':
		log_key = ''
		clientSA = SteamClient()
		r = clientSA.login(username=SAlogin,password=SApass)

		if r == EResult.OK:
			print(Xtag + 'Account Connected: [{0}:{1}]'.format(SAlogin,SApass))
		else:
			if r == EResult.LoggedInElsewhere:
				print('[XSteam] - Steam Error: Logged In Elsewhere')
			if r == EResult.NoConnection:
					print('[XSteam] - No Connection')
			elif r == EResult.InvalidPassword:
					print('[XSteam] - Invalid Password/Login')
			elif r == EResult.RateLimitExceeded:
				print('[XSteam] Steam Error: Try again later')
			elif r == EResult.AccountLoginDeniedThrottle:
				print('[XSteam] Login attempt failed, try to throttle response to possible attacker')
			elif r == EResult.AccountLoginDeniedNeedTwoFactor:
				twofactor = input(Xtfa + 'Введите 2FA-Code: ')
				d12 = clientSA.login(username=SAlogin,password=SApass,two_factor_code=twofactor)
				if d12 == EResult.OK:
					print('{0}Account Connected: [{1}:{2}]'.format(Xtag,SAlogin,SApass))
				else:
					if d12 == EResult.RateLimitExceeded:
						print('[XSteam] Steam Error: Try again later')
					elif d12 == EResult.AccountLoginDeniedThrottle:
						print('[XSteam] Login attempt failed, try to throttle response to possible attacker')
					elif d12 == EResult.TwoFactorCodeMismatch:
						print('[XSteam] - Введен неверный 2FA Code, повторите попытку.')
						twofactor = input(Xtfa + 'Введите 2FA-Code: ')
						d12 = clientSA.login(username=SAlogin,password=SApass,two_factor_code=twofactor)
						if d12 == EResult.OK:
							print('{0}Account Connected: [{1}:{2}]'.format(Xtag,SAlogin,SApass))
					elif clientSA.relogin_available:
						print(Xtag + 'Try relogin [{0}:{1}]'.format(SAlogin,SApass))
						clientSA.relogin()
		start = datetime.now()
		print('Start: ' + start.strftime("\nYear: %Y\nMonth: %B\nDay: %d\nTime: %H:%M:%S"))
		clientSA.set_ui_mode(3)
		clientSA.games_played(GamesToIdle)
		clientSA.change_status(persona_state=7)
		print(Xtag + 'Games started.')
		clientSA.run_forever()
	elif method == 'NewAccount':
		aoaLogin = input('[XSteam] Введите логин от аккаунта: ')
		aoaPass = input('[XSteam] Введите пароль от аккаунта: ')
		clientNA = SteamClient()
		r = clientNA.login(username=aoaLogin,password=aoaPass)
		if r == EResult.OK:
			print(Xtag + 'Account Connected: [{0}:{1}]'.format(aoaLogin,aoaPass))
		else:
			twofactor = input(Xtfa + 'Введите 2FA-Code: ')
			d12 = clientNA.login(username=aoaLogin,password=aoaPass,two_factor_code=twofactor)
			if d12 == EResult.OK:
				print('{0}Account Connected: [{1}:{2}] as {3}'.format(Xtag,aoaLogin,aoaPass,client.username))
				sessionid = client.session_id()
			else:
				print(Xerror + str(d12))
				if clientNA.relogin_available:
					print(Xtag + 'Try relogin [{0}:{1}]'.format(aoaLogin,aoaPass))
					clientNA.relogin()
		start = datetime.now()
		print('Start: ' + start.strftime("\nYear: %Y\nMonth: %B\nDay: %d\nTime: %H:%M:%S"))
		clientNA.set_ui_mode(3)
		clientNA.games_played(GamesToIdle)
		clientNA.change_status(persona_state=7)
		print(Xtag + 'Games started.')
		clientNA.run_forever()
	else:
		print('[XSteam Error]: Wrong method selected.')