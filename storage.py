import kivy

from kivy.uix.button import Button
from kivy.app import App

from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition

from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.properties import StringProperty,BooleanProperty

from json import dump as j_dump
from json import load as j_load
from codecs import open as co_open
from os import makedirs
from os.path import exists,dirname
from random import randint
from functools import partial

global all_details, tot_accs, confirmation, now_details,show_acc_no
confirmation = False
tot_accs,show_acc_no = 0,0
all_details = {}
now_details = {}

def encrypt_pass(password):
	key_enc = [121, 106, 59, 110, 62, 18, 28, 85, 8, 40, 83, 61, 25, 75, 43, 53, 4, 80, 44, 119, 68, 77, 29, 113, 64, 96, 112, 102, 54, 84, 6, 97, 36, 126, 120, 88, 98, 86, 17, 107, 34, 49, 26, 92, 71, 11, 60, 33, 122, 55, 35, 115, 37, 3, 67, 69, 31, 87, 70, 72, 99, 14, 51, 116, 50, 81, 24, 7, 117, 89, 21, 124, 47, 125, 73, 66, 12, 42, 38, 63, 79, 20, 9, 123, 76, 22, 91, 93, 19, 1, 16, 82, 46, 58, 127, 32, 100, 10, 78, 114, 101, 90, 74, 13, 105, 94, 23, 52, 2, 57, 41, 109, 104, 39, 95, 45, 65, 27, 5, 108, 118, 0, 56, 103, 48, 15, 111, 30]
	pos_enc = [24, 44, 29, 35, 41, 49, 27, 1, 31, 17, 37, 47, 0, 45, 3, 21, 14, 5, 4, 9, 36, 16, 7, 28, 2, 32, 13, 30, 46, 42, 22, 8, 10, 23, 43, 33, 48, 39, 19, 20, 34, 11, 25, 40, 26, 18, 12, 15, 38, 6]

	keys = []
	for i in range(len(password)):
		x = (ord(password[i]))
		keys.append(pos_enc[i]+key_enc[x])
	return(keys)

def decrypt_pass(keys):
	key_dcr = [121, 89, 108, 53, 16, 118, 30, 67, 8, 82, 97, 45, 76, 103, 61, 125, 90, 38, 5, 88, 81, 70, 85, 106, 66, 12, 42, 117, 6, 22, 127, 56, 95, 47, 40, 50, 32, 52, 78, 113, 9, 110, 77, 14, 18, 115, 92, 72, 124, 41, 64, 62, 107, 15, 28, 49, 122, 109, 93, 2, 46, 11, 4, 79, 24, 116, 75, 54, 20, 55, 58, 44, 59, 74, 102, 13, 84, 21, 98, 80, 17, 65, 91, 10, 29, 7, 37, 57, 35, 69, 101, 86, 43, 87, 105, 114, 25, 31, 36, 60, 96, 100, 27, 123, 112, 104, 1, 39, 119, 111, 3, 126, 26, 23, 99, 51, 63, 68, 120, 19, 34, 0, 48, 83, 71, 73, 33, 94]
	pos_dcr = [24, 44, 29, 35, 41, 49, 27, 1, 31, 17, 37, 47, 0, 45, 3, 21, 14, 5, 4, 9, 36, 16, 7, 28, 2, 32, 13, 30, 46, 42, 22, 8, 10, 23, 43, 33, 48, 39, 19, 20, 34, 11, 25, 40, 26, 18, 12, 15, 38, 6]

	dcr_pass = ''
	for i in range(len(keys)):
		dcr_pass += chr(key_dcr[((keys[i])-pos_dcr[i])])
	return dcr_pass

def write_json(dict_,file_path):
	ensure_dir(file_path)
	j_dump(dict_, co_open(file_path, 'w', encoding='utf-8'), separators=(',', ':'), sort_keys=True, indent=4)

def json_loader(filepath):
	file = open(filepath)
	dict_ = j_load(file)
	return dict_

def ensure_dir(file_path):
	directory = dirname(file_path)
	if not exists(directory):
		makedirs(directory)

def save_all_data():
	global all_details,tot_accs
	saver_dict = {}
	for i in range(tot_accs):
		this_dict = {}
		for j in (all_details[0]):
			this_dict[j] = encrypt_pass(all_details[i][j])
		saver_dict[i]=this_dict
	write_json(saver_dict,'all_data/details.json')

def load_all_data():
	new_dict = json_loader('all_data/details.json')
	global all_details,tot_accs
	tot_accs = len(new_dict)
	for i in range(tot_accs):
		this_dict = {}
		for j in (new_dict[str(0)]):
			this_dict[j] = decrypt_pass(new_dict[str(i)][j])
		all_details[i]=this_dict


class Confirmation_Popup(Popup):
	def __init__(self,**kwargs):
		super(Confirmation_Popup,self).__init__(**kwargs)
		self.title = "Do you want to save this Account"
		self.layout = GridLayout(cols=2, padding=10, spacing=5)
		self.size_hint = 0.32,0.2
		self.yes_button = Button(text="Yes", on_press=partial(self.set_confirmation,True))
		self.no_button = Button(text="No", on_press=partial(self.set_confirmation,False))
		self.layout.add_widget(self.yes_button)
		self.layout.add_widget(self.no_button)
		self.content = self.layout

	def set_confirmation(self,val,xxx):
		global confirmation
		confirmation = val
		self.dismiss()
		global all_details, tot_accs, now_details
		if(confirmation):
			all_details[tot_accs] = now_details
			print(all_details)
			tot_accs+=1
			save_all_data()

class LoginScreen(Screen):
	do_sum = StringProperty()
	def __init__(self,**kwargs):
		super(LoginScreen,self).__init__(**kwargs)
		self.x_1 = randint(1,2000)
		self.x_2 = randint(1,2000)
		self.x_sum = 0
		self.do_sum = str(self.x_1) + '  +  ' + str(self.x_2) + '  =  '

	def login_info(self):
		name_input = self.ids['name_input'].text
		pass_input = self.ids['pass_input'].text
		if(name_input == 'nil' and pass_input == 'pass'):
			sum_pre = int(self.ids['sum_input'].text)
			if(sum_pre == (self.x_1+self.x_2)):
				self.ids['pass_input'].text = ''
				self.manager.current = 'userhome_window'
				self.manager.transition.direction = 'up'

	def update_captcha(self):
		self.x_1 = randint(1,2000)
		self.x_2 = randint(1,2000)
		self.x_sum = 0
		self.do_sum = str(self.x_1) + '  +  ' + str(self.x_2) + '  =  '

	def super_login_info(self):
		pass

class UserScreen(Screen):
	def __init__(self,**kwargs):
		super(UserScreen,self).__init__(**kwargs)

class GetScreen(Screen):
	pass_val = BooleanProperty()
	def __init__(self,**kwargs):
		super(GetScreen,self).__init__(**kwargs)
		self.pass_val = True
	def search_by(self,cat,val):
		global search_cat, search_val
		search_cat = cat
		search_val = val
		self.manager.current = "result_window"
	def change_pass_val(self):
		self.pass_val = not(self.pass_val)

class ResScreen(Screen):
	def __init__(self,**kwargs):
		super(ResScreen,self).__init__(**kwargs)
		self.tot_buttons = 0
		self.refresh_button()

	def refresh_button(self):
		refresh_btn = Button(text="click here to refresh",on_press=self.search_by)
		self.add_widget(refresh_btn)

	def search_by(self,btn__):
		global all_details, tot_accs, search_cat, search_val
		self.clear_widgets()
		self.play = ScrollView(size_hint=(1, None), size=(Window.width, Window.height))
		self.roll = GridLayout(cols=1, spacing=10, size_hint_y=None)
		self.back_txt = "Go Back"
		print(len(all_details))
		back_btn_up = Button(text=self.back_txt,font_size=25,size_hint_y=None,height=40,on_press=self.goback)
		self.roll.bind(minimum_height=self.roll.setter('height'))
		self.roll.add_widget(back_btn_up)
		for i in range(tot_accs):
			if(all_details[i][search_cat]==search_val):
				btn_txt = "Site : " + all_details[i]["Site Name"] + "     Username : " + all_details[i]["Username"]
				this_button = Button(text=btn_txt,font_size=25,size_hint_y=None,height=40,background_color=(0,0,0,1),on_press=partial(self.show_acc,i))
				self.roll.add_widget(this_button)
		back_btn_down = Button(text=self.back_txt,font_size=25,size_hint_y=None,height=40,background_color=(0,0,0,1),on_press=self.goback)
		self.roll.add_widget(back_btn_down)
		self.add_widget(self.play)
		self.play.add_widget(self.roll)

	def show_acc(self,acc_no,_):
		global show_acc_no
		show_acc_no = acc_no
		self.clear_widgets()
		self.refresh_button()
		self.manager.current = "showacc_window"
		self.manager.transition.direction = 'left'

	def goback(self,_):
		self.clear_widgets()
		self.refresh_button()
		self.manager.current = "getpass_window"
		self.manager.transition.direction = 'right'

class ShowAllScreen(Screen):
	back_txt = StringProperty()
	def __init__(self,**kwargs):
		super(ShowAllScreen,self).__init__(**kwargs)
		self.refresh_button()

	def refresh_button(self):
		refresh_btn = Button(text="click here to refresh",on_press=self.add_all)
		self.add_widget(refresh_btn)

	def add_all(self,_):
		global tot_accs,all_details
		self.clear_widgets()
		self.play = ScrollView(size_hint=(1, None), size=(Window.width, Window.height))
		self.roll = GridLayout(cols=1, spacing=10, size_hint_y=None)
		self.back_txt = "Go Back"
		print(len(all_details))
		back_btn_up = Button(text=self.back_txt,font_size=25,size_hint_y=None,height=40,background_color=(0,0,0,1),on_press=self.gohome)
		self.roll.bind(minimum_height=self.roll.setter('height'))
		self.roll.add_widget(back_btn_up)
		for i in range(tot_accs):
			btn_txt = "Site : " + all_details[i]["Site Name"] + "     Username : " + all_details[i]["Username"]
			this_button = Button(text=btn_txt,font_size=25,size_hint_y=None,height=40,on_press=partial(self.show_acc,i))
			self.roll.add_widget(this_button)
		back_btn_down = Button(text=self.back_txt,font_size=25,size_hint_y=None,height=40,background_color=(0,0,0,1),on_press=self.gohome)
		self.roll.add_widget(back_btn_down)
		self.add_widget(self.play)
		self.play.add_widget(self.roll)

	def show_acc(self,acc_no,_):
		global show_acc_no
		show_acc_no = acc_no
		self.clear_widgets()
		self.refresh_button()
		self.manager.current = "showacc_window"

	def gohome(self,_):
		self.clear_widgets()
		self.refresh_button()
		self.manager.current = "userhome_window"
		self.manager.transition.direction = 'left'

class ShowScreen(Screen):
	write_txt = StringProperty()
	def __init__(self,**kwargs):
		super(ShowScreen,self).__init__(**kwargs)
		self.refresh_button()

	def refresh_button(self):
		refresh_btn = Button(text="click here to refresh",on_press=self.show_acc)
		self.add_widget(refresh_btn)

	def show_acc(self,_):
		global all_details,show_acc_no
		now_details = all_details[show_acc_no]
		self.clear_widgets()
		self.write_txt = "Site : " + now_details["Site"]
		self.write_txt += "\nSite Name : " + now_details["Site Name"]
		self.write_txt += "\nEmail-ID : " + now_details["Email-ID"]
		self.write_txt += "\nUsername : " + now_details["Username"]		
		self.write_txt += "\nPassword : " + now_details["Password"]	
		self.write_txt += "\nAcc. Details : " + now_details["Account details"]
		self.write_txt += "\nContact : " + now_details["Contact"]

		details_btn = Label(text=self.write_txt,halign="center",valign="center",font_size=30,pos_hint={"center_x":0.5,"center_y":0.5})
		home_btn = Button(text="Go Home",font_size=25,background_color=(0,0,0,1),color=(1,1,1,0.1),size_hint=(0.48,0.1),pos_hint={"center_x":0.25,"center_y":0.05},on_press=self.gohome)
		search_btn = Button(text="Search",font_size=25,background_color=(0,0,0,1),color=(1,1,1,0.1),size_hint=(0.48,0.1),pos_hint={"center_x":0.75,"center_y":0.05},on_press=self.gosearch)
		self.add_widget(details_btn)
		self.add_widget(home_btn)
		self.add_widget(search_btn)

	def gohome(self,_):
		self.clear_widgets()
		self.refresh_button()
		self.manager.current = "userhome_window"
		self.manager.transition.direction = 'left'

	def gosearch(self,_):
		self.clear_widgets()
		self.refresh_button()
		self.manager.current = "getpass_window"
		self.manager.transition.direction = 'left'

class NewScreen(Screen):
	pass_val = BooleanProperty()
	def __init__(self,**kwargs):
		super(NewScreen,self).__init__(**kwargs)
		self.pass_val = True
	def change_pass_val(self):
		self.pass_val = not(self.pass_val)

	def submit(self):
		global now_details
		now_details = {}
		now_details["Site"] = self.ids["site_input"].text
		now_details["Site Name"] = self.ids["sitename_input"].text		
		now_details["Email-ID"] = self.ids["email_input"].text
		now_details["Username"] = self.ids["username_input"].text		
		now_details["Password"] = self.ids["password_input"].text	
		now_details["Account details"] = self.ids["accdetails_input"].text
		now_details["Contact"] = self.ids["contact_input"].text

		new_popup = Confirmation_Popup()
		new_popup.open()

	def clear_data(self):
		self.ids["site_input"].text
		self.ids["sitename_input"].text = ''		
		self.ids["email_input"].text = ''
		self.ids["username_input"].text = ''
		self.ids["password_input"].text = ''
		self.ids["accdetails_input"].text = ''
		self.ids["contact_input"].text = ''

class MainClass(App):
	def build(self):
		ScreenMan = ScreenManagerbuild()

		ScreenMan.add_widget(UserScreen(name='userhome_window'))
		ScreenMan.add_widget(LoginScreen(name='login_window'))
		ScreenMan.add_widget(GetScreen(name='getpass_window'))
		ScreenMan.add_widget(NewScreen(name='newpass_window'))
		ScreenMan.add_widget(ResScreen(name='result_window'))
		ScreenMan.add_widget(ShowScreen(name='showacc_window'))
		ScreenMan.add_widget(ShowAllScreen(name='showall_window'))
		
		return ScreenMan

class ScreenManagerbuild(ScreenManager):
	pass

if __name__ == '__main__':
	load_all_data()
	print(all_details)
	MainClass().run()

"""
site name
site details
email id
username
password
account details
contact number



"""


