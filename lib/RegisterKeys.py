from libs import *
def RegisterKey():
	keys = []
	clientKey = SteamClient()

	with open('texts\keys.txt','r') as keysf:
		keys = keysf.read().split()
		print('[XSteam]: Ключи собраны')
	print('[XSteam] - Введите данные аккаунта, на который нужно активировать ключи.')
	rkLogin= input('[XSteam] Введите ваш логин: ')
	rkPass= input('[XSteam] Введите ваш пароль: ')
	rkLog = clientKey.login(username=rkLogin,password=rkPass)
	if rkLog == EResult.OK:
		print('[XSteam] - Account Connected: [{0}:{1}]'.format(rkLogin,rkPass))
		for keyW in keys:
			clientKey.register_product_key(keyW)
	else:
		if rkLog == EResult.NoConnection:
			print('[XSteam] - No Connection')

		elif rkLog == EResult.InvalidPassword:
			print('[XSteam] - Invalid Password/Login')

		elif rkLog == EResult.AccountLoginDeniedNeedTwoFactor:

			twofactor = input(Xtfa + 'Введите 2FA-Code: ')
			rkLog = clientKey.login(username=rkLogin,password=rkPass,two_factor_code=twofactor)
			if rkLog == EResult.OK:

				print('[XSteam] - Account Connected: [{0}:{1}]'.format(rkLogin,rkPass))

				for keyW in keys:
					clientKey.register_product_key(keyW)
		elif rkLog == EResult.TwoFactorCodeMismatch:
			print('[XSteam] - Введен неверный 2FA Code, повторите попытку.')
			twofactor = input(Xtfa + 'Введите 2FA-Code: ')
			rkLog = clientKey.login(username=rkLogin,password=rkPass,two_factor_code=twofactor)
			if rkLog == EResult.OK:
				print('{0}Account Connected: [{1}:{2}]'.format(Xtag,rkLogin,rkPass))
			elif rkLog == EResult.LoggedInElsewhere:
				print('[XSteam] - Steam Error: Logged In Elsewhere')
			elif clientKey.relogin_available:
				print(Xtag + 'Try relogin [{0}:{1}]'.format(rkLogin,rkPass))
				clientKey.relogin()
		elif rkLog == EResult.RateLimitExceeded:
			print('[XSteam] Steam Error: Try again later')
		elif rkLog == EResult.AccountLoginDeniedThrottle:
			print('[XSteam] Login attempt failed, try to throttle response to possible attacker')