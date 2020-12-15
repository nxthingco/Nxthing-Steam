from libs import *
from datetime import timedelta
def record():
	start = datetime.now()
	print('Start: ' + start.strftime("\nYear: %Y\nMonth: %B\nDay: %d\nTime: %H:%M:%S"))
	print(int(start.strftime('%H'))+3)
	while True:
	    now = datetime.now()
	    print('Now: ' + now.strftime("%H:%M:%S"), end='\r')
def GetTime():
	start = datetime.now()
	print('Now: ' + start.strftime("\nYear: %Y Month: %B Day: %d Time: %H:%M:%S"))