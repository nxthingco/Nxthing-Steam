import requests
from bs4 import BeautifulSoup
import re
import zipfile
url = 'https://nxthingco.github.io/Nxthing-Steam/'
url_download = 'https://github.com/nxthingco/Nxthing-Steam/archive/main.zip'

def CheckVersion(current_version):

	response = requests.get(url)
	soup = BeautifulSoup(response.text,'html.parser')
	classfind = soup.findAll('h1')
	version = re.split('Version\s+',classfind[2].text)
	del version[0]
	version = ''.join(version)
	print('Version on site: ' + str( version ) )

	if float(version) > float(current_version):
		print('Version is out of date')
		request_update = input('Обновить версию? (Y/N): ')

		if request_update == 'Y':
			update_program = requests.get(url_download)

			with open('update.zip','wb') as file:
				file.write(update_program.content)
				filezip = zipfile.ZipFile('update.zip','r')
				filezip.extractall()
				file.close()

		elif request_update == 'N': print('Starting..')
		else: print('Выбрано не верное действие.')

	elif float(version) == float(current_version): print('Current Version: ' + str(version))
	else: print('how?')