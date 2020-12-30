from libs import *
import tkinter as tk
from tkinter import *
from tkinter import scrolledtext
from tkinter import ttk
from ApiSteam import *
from GetSteamIDS import get_steam_info as gsi
from new_ParseSteamProfile import *

cur_path = os.path.dirname(__file__)
PathToFile = cur_path + '/texts/settings.json'

window = Tk()
window.title("Nxthing - Steam")
window.geometry('400x400')
window.resizable(width=False, height=False)

def center(win):
    win.update_idletasks()
    width = win.winfo_width()
    frm_width = win.winfo_rootx() - win.winfo_x()
    win_width = width + 2 * frm_width
    height = win.winfo_height()
    titlebar_height = win.winfo_rooty() - win.winfo_y()
    win_height = height + titlebar_height + frm_width
    x = win.winfo_screenwidth() // 2 - win_width // 2
    y = win.winfo_screenheight() // 2 - win_height // 2
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    win.deiconify()

def StartPr():
	MAIN_API_KEY = ent_api_key.get()
	MAIN_URL = ent_url.get()
	MAIN_STEAM_ID = 'steamid=' + str( gsi.SteamId(MAIN_URL) ) 
	MAIN_STEAM_IDS = 'steamids=' + str( gsi.SteamId(MAIN_URL) )
	ParseSteamProfile(MAIN_API_KEY,MAIN_URL)

def ClearLabels():
	ent_api_key.delete(0,100)
	ent_url.delete(0,100)
def LoadSettings():
	with open(PathToFile,'r') as rf:
		rdata = json.loads(rf.read())
		return rdata;

def SaveSettings():
	with open(PathToFile,'w') as sf:
		data = {
			"MAIN_API_KEY":ent_api_key.get(),
			"MAIN_URL":ent_url.get(),
			"MAIN_STEAM64ID":str( gsi.SteamId(MAIN_URL) ) ,
		}
		try:
			json.dump(data,sf)
			print('Данные сохранены.')
		except:
			print('Не сохранено!')
		sf.close()

label1 = tk.Label(text=" Nxthing - Steam", font=('Arial-Bold',15))
label1.grid(row=0, column=0, sticky="n")

frm_form = tk.Frame(relief=tk.FLAT, borderwidth=3)
	 
lbl_api_key = tk.Label(master=frm_form, text="API Key:")
ent_api_key = tk.Entry(master=frm_form, width=50)
ent_api_key.insert(0,MAIN_API_KEY)
lbl_api_key.grid(row=0, column=0, sticky="e")
ent_api_key.grid(row=0, column=1)

lbl_url = tk.Label(master=frm_form, text="URL:")
ent_url = tk.Entry(master=frm_form, width=50)
ent_url.insert(0,MAIN_URL)
lbl_url.grid(row=1, column=0, sticky="e")
ent_url.grid(row=1, column=1)
frm_form.grid()

btn_submit = tk.Button(text="Начать программу",relief=tk.FLAT,command=StartPr)
btn_save = tk.Button(text="Сохранить",relief=tk.FLAT,command=SaveSettings)
btn_clear = tk.Button(text="Очистить",relief=tk.FLAT,command=ClearLabels)

btn_submit.grid(row=2, column=0,sticky='w', padx=10, ipadx=10)
btn_save.grid(row=2, column=0,sticky='s', padx=10, ipadx=10)
btn_clear.grid(row=2, column=0,sticky='e', ipadx=10)

r = LoadSettings()
print(r['MAIN_API_KEY'])

center(window)
window.mainloop()
print(MAIN_URL)