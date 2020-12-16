from libs import *

url = 'https://steamcommunity.com/profiles/76561199099401551'
badge_response = requests.get(url + '/badges/1')
soup_badge = BeautifulSoup(badge_response.text,'html.parser')
MemberSince = soup_badge.find('div',class_='badge_description')
if MemberSince:
	MemberSince = re.split('\s+',''.join(MemberSince))
	del MemberSince[0],MemberSince[-1]
	print(' '.join(MemberSince))
else:
	print('Невозможно определить дату создания аккаунта')