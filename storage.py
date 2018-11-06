import kivy

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

global now_user, now_pass, now_pin, all_user, all_pass, all_user_num, all_enc_keys, all_dcr_keys
now_user, now_pass, now_pin = 0, 0, 00000
all_enc_keys , all_dcr_keys = {} , {}
all_user, all_pass, all_user_num = {} , {} , {}
world_all_details = {}

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
	global world_all_details,world_tot_accs
	write_json(world_all_details,'all_data/details.json')

def load_all_data():
	global world_all_details,world_tot_accs
	details = json_loader('all_data/details.json')
	for i in range(len(details)):
		world_all_details[i] = {}
		for j in range(len(details[str(i)])):
			world_all_details[i][j] = details[str(i)][str(j)]
	world_tot_accs = len(world_all_details)

def encrypt_pass(password,my_key=-1):
	if(my_key==-1):
		global now_pin
		my_key = now_pin
	global all_keys
	key_enc = all_enc_keys[my_key//1000]
	pos_enc = all_enc_keys[my_key%1000]
	keys = []
	for i in range(len(password)):
		x = (ord(password[i]))
		keys.append(pos_enc[i]+key_enc[x])
	return(keys)

def decrypt_pass(keys,my_key=-1):
	if(my_key==-1):
		global now_pin
		my_key = now_pin
	global all_keys
	key_dcr = all_dcr_keys[my_key//1000]
	pos_dcr = all_enc_keys[my_key%1000]
	dcr_pass = ''
	for i in range(len(keys)):
		dcr_pass += chr(key_dcr[((keys[i])-pos_dcr[i])])
	return dcr_pass

def load_all_keys():
	global all_enc_keys, all_dcr_keys
	now_dict = json_loader('all_data/all_keys.json')
	for i in range(len(now_dict)):
		now_dcr = [0 for kk in range(128)]
		all_enc_keys[i] = now_dict[str(i)]
		for j in range(128):
			now_dcr[all_enc_keys[i][j]] = j
		all_dcr_keys[i] = now_dcr

def load_all_user():
	global all_user, all_pass, all_user_num
	now_dict = json_loader('all_data/all_user_details.json')
	for i in range(len(now_dict)):
		all_user[i] = decrypt_pass(now_dict[str(i)]["name"],356349)
		all_pass[i] = decrypt_pass(now_dict[str(i)]["pass"],356349)
		all_user_num[decrypt_pass(now_dict[str(i)]["name"],356349)] = i

def save_all_user():
	global all_user, all_pass
	now_dict = {}
	for i in range(len(all_user)):
		this_dict = {}
		this_dict["name"] = encrypt_pass(all_user[i],356349)
		this_dict["pass"] = encrypt_pass(all_pass[i],356349)
		now_dict[i] = this_dict
	write_json(now_dict,'all_data/all_user_details.json')

def load_save():
	save_all_user()
	load_all_user()
	save_all_data()
	load_all_data()


class Change_Popup(Popup):
	def __init__(self,**kwargs):
		super(Change_Popup,self).__init__(**kwargs)
		global popup_mode
		self.title = "Enter new " + popup_mode
		self.layout = GridLayout(cols=1, padding=10, spacing=5)
		self.size_hint = 0.33,0.3

		self.text_input = TextInput(font_size=25,id="new_str")
		self.ok_button = Button(text="Ok", on_press=self.change)
		self.layout.add_widget(self.text_input)
		self.layout.add_widget(self.ok_button)
		self.content = self.layout

	def change(self,_):
		self.dismiss()
		global popup_mode
		if (popup_mode=="Username"):
			new_user = self.text_input.text
			name_exist = False
			try:
				all_user_num[name_input]
				name_exist = True
			except:
				pass
			global now_user
			now_user = new_user
		elif (popup_mode=="Password"):
			new_pass = self.text_input.text
			global all_pass
			all_pass[now_user] = new_pass

class Confirmation_Popup(Popup):
	def __init__(self,**kwargs):
		super(Confirmation_Popup,self).__init__(**kwargs)
		global popup_mode
		self.title = "Do you want to " + popup_mode + " this Account"
		self.layout = GridLayout(cols=2, padding=10, spacing=5)
		self.size_hint = 0.33,0.2
		self.yes_button = Button(text="Yes", on_press=partial(self.set_confirmation,True))
		self.no_button = Button(text="No", on_press=partial(self.set_confirmation,False))
		self.layout.add_widget(self.yes_button)
		self.layout.add_widget(self.no_button)
		self.content = self.layout

	def set_confirmation(self,val,xxx):
		global confirmation
		confirmation = val
		self.dismiss()
		global world_all_details, world_tot_accs, now_details, show_acc_no, now_user, now_pin
		if(confirmation and popup_mode=="Delete"):
			for i in range(show_acc_no,len(world_all_details[now_user])-1):
				world_all_details[now_user][i] = world_all_details[now_user][i+1]
			del world_all_details[now_user][world_tot_accs-1]
		if(confirmation and popup_mode=="Submit"):
			new_details = {}
			for j in now_details:
				new_details[j] = encrypt_pass(now_details[j],now_pin)
			world_all_details[now_user][len(world_all_details[now_user])] = new_details

		if(confirmation and popup_mode=="Edit"):
			new_details = {}
			for j in now_details:
				new_details[j] = encrypt_pass(now_details[j],now_pin)
			world_all_details[now_user][show_acc_no] = new_details
		if(confirmation):
			save_all_data()

class ResScreen(Screen):
	def __init__(self,**kwargs):
		super(ResScreen,self).__init__(**kwargs)
		self.tot_buttons = 0
		self.refresh_button()

	def refresh_button(self):
		refresh_btn = Button(text="click here to refresh",on_press=self.search_by)
		self.add_widget(refresh_btn)

	def on_pre_enter(self):
		self.search_by('nothing')

	def search_by(self,btn__):
		global world_all_details, now_user, search_cat, search_val,now_pin
		self.clear_widgets()
		self.play = ScrollView(size_hint=(1, None), size=(Window.width, Window.height))
		self.roll = GridLayout(cols=1, spacing=10, size_hint_y=None)
		self.back_txt = "Go Back"
		back_btn_up = Button(text=self.back_txt,font_size=25,size_hint_y=None,height=40,background_color=(0,0,0,1),on_press=self.goback)
		self.roll.bind(minimum_height=self.roll.setter('height'))
		self.roll.add_widget(back_btn_up)
		for i in range(len(world_all_details[now_user])):
			xxx = decrypt_pass(world_all_details[now_user][i][search_cat],now_pin)
			if search_val in xxx:
				btn_txt = "Site : " + decrypt_pass(world_all_details[now_user][i]["Site Name"],now_pin) + "     Username : " + decrypt_pass(world_all_details[now_user][i]["Username"],now_pin)
				this_button = Button(text=btn_txt,font_size=25,size_hint_y=None,height=40,on_press=partial(self.show_acc,i))
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

class ShowScreen(Screen):
	write_txt = StringProperty()
	def __init__(self,**kwargs):
		super(ShowScreen,self).__init__(**kwargs)
		self.refresh_button()

	def refresh_button(self):
		refresh_btn = Button(text="click here to refresh",on_press=self.show_acc)
		self.add_widget(refresh_btn)

	def on_pre_enter(self):
		self.show_acc('nothing')

	def show_acc(self,_):
		global all_details,show_acc_no,now_user,now_pin
		now_enc_details = world_all_details[now_user][show_acc_no]
		now_details = {}
		for j in now_enc_details:
			now_details[j] = decrypt_pass(now_enc_details[j],now_pin)
		self.clear_widgets()

		edit_btn = Button(text="Edit",font_size=25,background_color=(0,0,0,1),color=(1,1,1,0.1),size_hint=(0.48,0.1),pos_hint={"center_x":0.25,"center_y":0.95},on_press=self.edit_this)
		del_btn = Button(text="Delete",font_size=25,background_color=(0,0,0,1),color=(1,1,1,0.1),size_hint=(0.48,0.1),pos_hint={"center_x":0.75,"center_y":0.95},on_press=self.delete_this)
		self.add_widget(edit_btn)
		self.add_widget(del_btn)

		self.write_txt = "Site : " + now_details["Site"]
		self.write_txt += "\nSite Name : " + now_details["Site Name"]
		self.write_txt += "\nEmail-ID : " + now_details["Email-ID"]
		self.write_txt += "\nUsername : " + now_details["Username"]		
		self.write_txt += "\nPassword : " + now_details["Password"]	
		self.write_txt += "\nAcc. Details : " + now_details["Account Details"]
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

	def edit_this(self,_):
		self.clear_widgets()
		self.refresh_button()
		self.manager.current = "edit_window"
		self.manager.transition.direction = 'up'

	def delete_this(self,_):
		global popup_mode
		popup_mode = "Delete"
		new_popup = Confirmation_Popup()
		new_popup.open()
		self.manager.current = "userhome_window"
		self.manager.transition.direction = 'left'

class ShowAllScreen(Screen):
	back_txt = StringProperty()
	def __init__(self,**kwargs):
		super(ShowAllScreen,self).__init__(**kwargs)
		self.refresh_button()

	def refresh_button(self):
		refresh_btn = Button(text="click here to refresh",on_press=self.add_all)
		self.add_widget(refresh_btn)

	def on_pre_enter(self):
		self.add_all('nothing')

	def add_all(self,_):
		global world_tot_accs,world_all_details,now_user,now_pin
		self.clear_widgets()
		self.play = ScrollView(size_hint=(1, None), size=(Window.width, Window.height))
		self.roll = GridLayout(cols=1, spacing=10, size_hint_y=None)
		self.back_txt = "Go Back"
		back_btn_up = Button(text=self.back_txt,font_size=25,size_hint_y=None,height=40,background_color=(0,0,0,1),on_press=self.gohome)
		self.roll.bind(minimum_height=self.roll.setter('height'))
		self.roll.add_widget(back_btn_up)
		for i in range(len(world_all_details[now_user])):
			btn_txt = "Site : " + decrypt_pass(world_all_details[now_user][i]["Site Name"],now_pin) + "     Username : " + decrypt_pass(world_all_details[now_user][i]["Username"],now_pin)
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

class EditScreen(Screen):
	pass_val = BooleanProperty()
	def __init__(self,**kwargs):
		super(EditScreen,self).__init__(**kwargs)
		self.pass_val = True
	def change_pass_val(self):
		self.pass_val = not(self.pass_val)

	def on_pre_enter(self):
		self.fill_form()

	def fill_form(self):
		global show_acc_no,all_details,now_user,now_pin
		now_enc = world_all_details[now_user][show_acc_no]
		now = {}
		for j in now_enc:
			now[j] = decrypt_pass(now_enc[j],now_pin)
		self.ids["site_input"].text = now["Site"]
		self.ids["sitename_input"].text = now["Site Name"]
		self.ids["email_input"].text = now["Email-ID"]
		self.ids["username_input"].text = now["Username"]
		self.ids["password_input"].text = now["Password"]
		self.ids["accdetails_input"].text = now["Account Details"]
		self.ids["contact_input"].text = now["Contact"]

	def save(self):
		global now_details
		now_details = {}
		now_details["Site"] = self.ids["site_input"].text
		now_details["Site Name"] = self.ids["sitename_input"].text		
		now_details["Email-ID"] = self.ids["email_input"].text
		now_details["Username"] = self.ids["username_input"].text		
		now_details["Password"] = self.ids["password_input"].text	
		now_details["Account Details"] = self.ids["accdetails_input"].text
		now_details["Contact"] = self.ids["contact_input"].text

		global popup_mode
		popup_mode = "Edit"
		new_popup = Confirmation_Popup()
		new_popup.open()
		self.clear_data()

	def clear_data(self):
		self.ids["site_input"].text = ''
		self.ids["sitename_input"].text = ''
		self.ids["email_input"].text = ''
		self.ids["username_input"].text = ''
		self.ids["password_input"].text = ''
		self.ids["accdetails_input"].text = ''
		self.ids["contact_input"].text = ''

class UserScreen(Screen):
	def __init__(self,**kwargs):
		super(UserScreen,self).__init__(**kwargs)

class LoginScreen(Screen):
	do_sum = StringProperty()
	def __init__(self,**kwargs):
		super(LoginScreen,self).__init__(**kwargs)
		self.x_1 = randint(1,2000)
		self.x_2 = randint(1,2000)
		self.x_sum = 0
		self.do_sum = str(self.x_1) + '  +  ' + str(self.x_2) + '  =  '

	def on_pre_enter(self):
		self.update_captcha()

	def login_info(self):
		global now_user, now_pass, now_pin, all_user, all_pass, all_user_num
		name_input = self.ids['name_input'].text
		pass_input = self.ids['pass_input'].text
		try:
			now_user = all_user_num[name_input]
			now_pin = int(self.ids['pin_input'].text)
			if(pass_input == all_pass[now_user]):
				sum_pre = int(self.ids['sum_input'].text)
				if(sum_pre == (self.x_1+self.x_2)):
					self.ids['pass_input'].text = ''
					self.manager.current = 'userhome_window'
					self.manager.transition.direction = 'up'
		except:
			pass

	def signup_info(self):
		sum_pre = int(self.ids['sum_input'].text)
		if(sum_pre == (self.x_1+self.x_2)):
			global now_user, now_pin, all_user, all_pass, all_user_num, world_all_details, world_tot_accs
			name_input = self.ids['name_input'].text
			pass_input = self.ids['pass_input'].text
			now_pin = int(self.ids['pin_input'].text)
			name_exist = False
			try:
				all_user_num[name_input]
				name_exist = True
			except:
				pass
			if (not name_exist):
				now_user = len(all_user)
				all_user[now_user] = name_input
				all_pass[now_user] = pass_input
				all_user_num[name_input] = now_user
				self.manager.current = 'userhome_window'
				self.manager.transition.direction = 'up'
				world_all_details[world_tot_accs] = {}
				world_tot_accs += 1
				load_save()
				self.ids["name_input"].text = ""
				self.ids["pass_input"].text = ""
				self.ids["pin_input"].text = ""
			if name_exist:
				self.ids["name_input"].text = "username is taken"
				self.ids["pass_input"].text = ""
				self.ids["pin_input"].text = ""

	def update_captcha(self):
		self.x_1 = randint(1,2000)
		self.x_2 = randint(1,2000)
		self.x_sum = 0
		self.do_sum = str(self.x_1) + '  +  ' + str(self.x_2) + '  =  '

	def super_login_info(self):
		pass

class SettingScreen(Screen):
	def __init__(self,**kwargs):
		super(SettingScreen,self).__init__(**kwargs)

	def change(self):
		self.manager.current = 'change_window'
		self.manager.transition.direction = 'up'

class ChangeScreen(Screen):
	def __init__(self,**kwargs):
		super(ChangeScreen,self).__init__(**kwargs)

	def change_fun(self,mode):
		global all_pass, now_user
		in_pass = self.ids["pass_input"].text
		if(in_pass == all_pass[now_user]):
			if(mode == "name"):
				global all_user_num, all_user
				new_name = self.ids["change_name_input"].text
				name_exist = False
				try:
					all_user_num[new_name]
					name_exist = True
				except:
					pass
				if not name_exist:
					del all_user_num[all_user[now_user]]
					all_user_num[new_name] = now_user
					all_user[now_user] = new_name
					self.ids["status"].text = "UserName Changed"
					self.ids["status"].color = (0,1,0,0.5)
					load_save()
				if name_exist:
					self.ids["status"].text = "UserName Already Taken"
					self.ids["status"].color = (1,0,0,1)
			if(mode == "pass"):
				global all_pass, now_user
				new_pass = self.ids["change_pass_input"].text
				con_pass = self.ids["confirm_pass_input"].text
				if (new_pass == con_pass):
					all_pass[now_user] = new_pass
					self.ids["status"].text = "Password Changed"
					self.ids["status"].color = (0,1,0,0.5)
					load_save()
				else:
					self.ids["status"].text = "New Password & Confirm Password are not matching"
					self.ids["status"].color = (1,0,0,1)
			if(mode == "pin"):
				global all_pin, now_user
				go = True
				try:
					new_pin = int(self.ids["change_pin_input"].text)
					con_pin = int(self.ids["confirm_pin_input"].text)
				except:
					go = False
				if(go):
					if(new_pin == con_pin):
						global world_all_details,now_pin
						for i in range(len(world_all_details[now_user])):
							for j in (world_all_details[now_user][0]):
								now_word = decrypt_pass(world_all_details[now_user][i][j],now_pin)
								world_all_details[now_user][i][j] = encrypt_pass(now_word,new_pin)
						now_pin = new_pin
						load_save()
						self.ids["status"].text = "Pin Changed"
						self.ids["status"].color = (0,1,0,0.5)
					else:
						self.ids["status"].text = "New Pin & Confirm Pin are not matching"
						self.ids["status"].color = (1,0,0,1)
				else:
					self.ids["status"].text = "Pin can be Numbers only"
					self.ids["status"].color = (1,0,0,1)
		else:
			self.ids["status"].text = "Password is Wrong"
			self.ids["status"].color = (1,0,0,1)


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
		now_details["Account Details"] = self.ids["accdetails_input"].text
		now_details["Contact"] = self.ids["contact_input"].text

		global popup_mode
		popup_mode = "Submit"
		new_popup = Confirmation_Popup()
		new_popup.open()
		# self.clear_data()

	def clear_data(self):
		self.ids["site_input"].text = ''
		self.ids["sitename_input"].text = ''		
		self.ids["email_input"].text = ''
		self.ids["username_input"].text = ''
		self.ids["password_input"].text = ''
		self.ids["accdetails_input"].text = ''
		self.ids["contact_input"].text = ''

class MainClass(App):
	def build(self):
		ScreenMan = ScreenManagerbuild()

		ScreenMan.add_widget(LoginScreen(name='login_window'))
		ScreenMan.add_widget(ChangeScreen(name='change_window'))
		ScreenMan.add_widget(UserScreen(name='userhome_window'))
		ScreenMan.add_widget(SettingScreen(name='setting_window'))
		ScreenMan.add_widget(GetScreen(name='getpass_window'))
		ScreenMan.add_widget(NewScreen(name='newpass_window'))
		ScreenMan.add_widget(ResScreen(name='result_window'))
		ScreenMan.add_widget(ShowScreen(name='showacc_window'))
		ScreenMan.add_widget(EditScreen(name='edit_window'))
		ScreenMan.add_widget(ShowAllScreen(name='showall_window'))
		
		return ScreenMan

class ScreenManagerbuild(ScreenManager):
	pass

if __name__ == '__main__':
	load_all_keys()
	load_all_user()
	load_all_data()
	MainClass().run()


