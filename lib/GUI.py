from libs import *
import tkinter as tk
from tkinter import *
from tkinter import scrolledtext
from tkinter import ttk
from ApiSteam import *
from GetSteamIDS import get_steam_info as gsi
from new_ParseSteamProfile import *
from SteamIdle import *

cur_path = os.path.dirname(__file__)
PathToFile = cur_path + '/texts/settings.json'
def OpenGui():
	window = Tk()
	window.title("Nxthing - Steam")
	#window.geometry('400x400')
	window.resizable(width=False, height=False)

	def IdleGui(): 
		login = ent_login.get()
		password = ent_pass.get()
		idle('SingleAccount',login,password)

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
		ent_login.delete(0,100)
		ent_pass.delete(0,100)

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
				"Last_Login": ent_login.get(),
				"Last_Pass": ent_pass.get(),
			}
			try:
				json.dump(data,sf)
				print('Данные сохранены.')
			except:
				print('Не сохранено!')
			sf.close()

	r = LoadSettings()
	print('Api Key: ' + str( r['MAIN_API_KEY'] ) )

	log_insert,pass_insert = r['Last_Login'],r['Last_Pass']

	# LABEL NXTHING STEAM
	label1 = tk.Label(text=" Nxthing - Steam", font=('Arial-Bold',15)).pack()

	frm_form = tk.Frame(relief=tk.FLAT, borderwidth=3)
		 
	# GET API ---------	 
	lbl_api_key = tk.Label(master=frm_form, text="API Key:").pack()
	ent_api_key = tk.Entry(master=frm_form, width=50)
	ent_api_key.insert(0,MAIN_API_KEY)
	ent_api_key.pack()

	# GET URL ---------	 
	lbl_url = tk.Label(master=frm_form, text="URL:").pack()
	ent_url = tk.Entry(master=frm_form, width=50)
	ent_url.insert(0,MAIN_URL)
	ent_url.pack()

	# GET LOGIN,PASS FOR IDLE ---------	 
	lbl_login = tk.Label(master=frm_form, text="Login:").pack()
	ent_login = tk.Entry(master=frm_form, width=50)
	ent_login.insert(0,log_insert)
	ent_login.pack()

	lbl_pass = tk.Label(master=frm_form, text="Pass:").pack()
	ent_pass = tk.Entry(master=frm_form, width=50)
	ent_pass.insert(0,pass_insert)
	ent_pass.pack()
	frm_form.pack()

	btn_submit = tk.Button(text="Начать парсинг",relief=tk.FLAT,command=StartPr).pack(side=LEFT)
	btn_idle = tk.Button(text='Начать буст',relief=tk.FLAT,command=IdleGui).pack(side=LEFT)
	btn_save = tk.Button(text="Сохранить",relief=tk.FLAT,command=SaveSettings).pack(side=LEFT)
	btn_clear = tk.Button(text="Очистить",relief=tk.FLAT,command=ClearLabels).pack(side=LEFT)

	r = LoadSettings()

	center(window)
	window.mainloop()