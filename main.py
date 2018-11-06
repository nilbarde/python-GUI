import kivy

from kivy.app import App

from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.uix.behaviors import ButtonBehavior
from kivy.properties import StringProperty,BooleanProperty
from kivy.uix.videoplayer import VideoPlayer
from kivy.core.audio import SoundLoader
from kivy.uix.image import Image
from kivy.graphics import Color, Ellipse, Rectangle, RoundedRectangle
from kivy.uix.slider import Slider

from functools import partial
from random import shuffle, randint
from datetime import datetime
import threading
import time

from os_funs import *
from json_funs import *

def get_ext(file_name):
	global file_exts
	found_ext = False
	deep = 0
	while (found_ext==False and deep<6):
		deep += 1
		if(file_name[-deep]=="."):
			ext = file_name[-deep+1:]
			found_ext = True
	if(found_ext):
		for type_ in file_exts:
			if(ext.lower() in file_exts[type_]):
				my_type = type_
				return ext,my_type
	else:
		return "none","unknown"
	return ext,"unknown"

class ImageButton(ButtonBehavior, Image):
	pass

class HomeScreen(Screen):
	def __init__(self,**kwargs):
		super(HomeScreen,self).__init__(**kwargs)
		global now_folder
		self.path_width, self.path_height = 1.0, 0.1
		self.path_x, self.path_y = 0.5, 0.95
		self.folders_width, self.folders_height = 1.0, 0.4
		self.folders_x, self.folders_y = 0.5, 0.65
		self.files_width, self.files_height = 1.0, 0.4
		self.files_x, self.files_y = 0.5, 0.2

	def on_pre_enter(self):
		self.clear_widgets()
		global now_folder
		now_folder = now_folder.replace("//","/")
		print("__",now_folder)
		self.folders = get_folders(now_folder,1)
		self.files = get_files(now_folder,1)
		self.show_screen()

	def show_screen(self):
		self.add_path_scroll()
		self.add_folder_scroll()
		self.add_files_scroll()
		# threading.Thread(target=self.add_path_scroll).start()
		# threading.Thread(target=self.add_folder_scroll).start()
		# threading.Thread(target=self.add_files_scroll).start()

	def add_path_scroll(self):
		self.play_direc = ScrollView(size_hint=(self.path_width, self.path_height),pos_hint={"center_x":self.path_x,"center_y":self.path_y}, size=(Window.width, Window.height))
		self.roll_direc = GridLayout(cols=100,spacing=5, size_hint_x=None,padding=10)
		self.roll_direc.bind(minimum_width=self.roll_direc.setter('width'))
		self.play_direc.add_widget(self.roll_direc)
		self.add_widget(self.play_direc)

		prev_folders = now_folder[1:].split("/")
		print(prev_folders)
		self.roll_direc.cols = len(prev_folders)
		path_name = ""
		for old_fold in prev_folders:
			if(old_fold != ""):
				path_name += "/" + old_fold
				fold_button = Button(text=old_fold,font_size=20,size_hint_x=None,font_name=bold_font,on_press=partial(self.open_folder,path_name))
				fold_button.bind(width=lambda s,w: s.setter("text_size")(s,(w,None)))
				fold_button.bind(texture_size=fold_button.setter("size"))
				self.roll_direc.add_widget(fold_button)

	
	def add_folder_scroll(self):
		self.play_folds = ScrollView(size_hint=(self.folders_width, self.folders_height),pos_hint={"center_x":self.folders_x,"center_y":self.folders_y}, size=(Window.width, Window.height))
		self.roll_folds = GridLayout(cols=3,spacing=5,size_hint_y=None,padding=10)
		self.roll_folds.bind(minimum_height=self.roll_folds.setter('height'))

		self.play_folds.add_widget(self.roll_folds)
		self.add_widget(self.play_folds)

		for folder in self.folders:
			folder_name = (folder.split("/"))[-2]
			fold_button = Button(text=folder_name,font_size=20,size_hint_x=0.7,valign="center",halign="left",size_hint_y=None,font_name=bold_font,on_press=partial(self.open_folder,folder))
			fold_button.bind(width=lambda s,w: s.setter("text_size")(s,(w,None)))
			fold_button.bind(texture_size=fold_button.setter("size"))
			self.roll_folds.add_widget(fold_button)
			fold_size = "1" #get_size(folder)
			fold_button = Button(text=fold_size,font_size=20,size_hint_x=0.15,valign="center",halign="center",size_hint_y=None,font_name=bold_font,on_press=partial(self.open_folder,folder))
			fold_button.bind(width=lambda s,w: s.setter("text_size")(s,(w,None)))
			fold_button.bind(texture_size=fold_button.setter("size"))
			self.roll_folds.add_widget(fold_button)
			fold_date = get_modified_time(folder)
			fold_button = Button(text=fold_date,font_size=20,size_hint_x=0.15,valign="center",halign="center",size_hint_y=None,font_name=bold_font,on_press=partial(self.open_folder,folder))
			fold_button.bind(width=lambda s,w: s.setter("text_size")(s,(w,None)))
			fold_button.bind(texture_size=fold_button.setter("size"))
			self.roll_folds.add_widget(fold_button)

	def add_files_scroll(self):
		self.play_files = ScrollView(size_hint=(self.files_width, self.files_height),pos_hint={"center_x":self.files_x,"center_y":self.files_y}, size=(Window.width, Window.height))
		self.roll_files = GridLayout(cols=3,spacing=5,size_hint_y=None,padding=10)
		self.roll_files.bind(minimum_height=self.roll_files.setter('height'))

		self.play_files.add_widget(self.roll_files)
		self.add_widget(self.play_files)

		for file_name_big in self.files:
			file_name = ((file_name_big.split("/"))[-1])
			file_button = Button(text=file_name,font_size=20,size_hint_x=0.7,valign="center",halign="center",size_hint_y=None,font_name=bold_font,on_press=partial(self.open_file,file_name_big))
			file_button.bind(width=lambda s,w: s.setter("text_size")(s,(w,None)))
			file_button.bind(texture_size=file_button.setter("size"))
			self.roll_files.add_widget(file_button)
			file_size = get_size(file_name_big)
			file_button = Button(text=file_size,font_size=20,size_hint_x=0.15,valign="center",halign="center",size_hint_y=None,font_name=bold_font,on_press=partial(self.open_file,file_name_big))
			file_button.bind(width=lambda s,w: s.setter("text_size")(s,(w,None)))
			file_button.bind(texture_size=file_button.setter("size"))
			self.roll_files.add_widget(file_button)
			file_date = get_modified_time(file_name_big)
			file_button = Button(text=file_date,font_size=20,size_hint_x=0.15,valign="center",halign="center",size_hint_y=None,font_name=bold_font,on_press=partial(self.open_file,file_name_big))
			file_button.bind(width=lambda s,w: s.setter("text_size")(s,(w,None)))
			file_button.bind(texture_size=file_button.setter("size"))
			self.roll_files.add_widget(file_button)

	def open_folder(self,folder_name,_="_"):
		global now_folder
		print("opening ",folder_name)
		now_folder = folder_name
		self.on_pre_enter()

	def open_file(self,file_name,_="_"):
		global file_exts, now_file
		now_file = file_name
		my_type = "unknown"
		ext, my_type = get_ext(file_name)
		if(my_type != "unknown"):
			self.manager.current = my_type

class ImageScreen(Screen):
	def __init__(self,**kwargs):
		super(ImageScreen,self).__init__(**kwargs)
		global now_folder
		self.name_width, self.name_height = 0.6,0.08
		self.name_x, self.name_y = 0.5, 0.95
		self.back_width, self.back_height = 0.2, 0.1
		self.back_x, self.back_y = 0.1, 0.95
		self.image_width, self.image_height = 0.9, 0.7
		self.image_x, self.image_y = 0.5, 0.55
		self.trav_width, self.trav_height = (1.0 - self.image_width)/2, self.image_height
		self.trav_x_next, self.trav_x_prev, self.trav_y = 1 - (self.trav_width/2), self.trav_width/2, self.image_y
		self.scroll_width, self.scroll_height = 1.0, 0.2
		self.scroll_x, self.scroll_y = 0.5, 0.1
		self.scroll_nums = 10

	def on_pre_enter(self):
		global now_folder, now_file
		self.files = get_files(now_folder,1)
		self.now_id = -1
		self.ext,self.my_type = get_ext(now_file)
		self.images = []
		self.get_images()
		self.clear_widgets()
		self.show_screen()

	def show_screen(self):
		self.add_title()
		self.add_scroll()

	def add_title(self):
		global now_file, bold_font
		self.name_label = Label(text=((now_file.split("/"))[-1]),font_size=25,size_hint=(self.name_width,self.name_height),pos_hint={"center_x":self.name_x,"center_y":self.name_y},valign="center",halign="center",font_name=bold_font)
		self.name_label.bind(width=lambda s,w: s.setter("text_size")(s,(w,None)))
		self.name_label.bind(texture_size=self.name_label.setter("size"))
		self.add_widget(self.name_label)
		self.back_btn = Button(text="<-",font_size=50,background_color=(0,0,0,1),size_hint=(self.back_width,self.back_height),pos_hint={"center_x":self.back_x,"center_y":self.back_y},valign="center",halign="center",font_name=bold_font,on_press=self.go_home)
		self.back_btn.bind(width=lambda s,w: s.setter("text_size")(s,(w,None)))
		self.back_btn.bind(texture_size=self.back_btn.setter("size"))
		self.add_widget(self.back_btn)
		self.image = Image(source=now_file,pos_hint={"center_x":self.image_x,"center_y":self.image_y},size_hint=(self.image_width,self.image_height),keep_ratio=True,allow_stretch=True)
		self.add_widget(self.image)
		if(self.now_id != (len(self.images)-1)):
			self.next_btn = Button(text=">",font_size=50,background_color=(0,0,0,1),size_hint=(self.trav_width,self.trav_height),pos_hint={"center_x":self.trav_x_next,"center_y":self.trav_y},valign="center",halign="center",font_name=bold_font,on_press=partial(self.change_photo,self.now_id+1))
			self.next_btn.bind(width=lambda s,w: s.setter("text_size")(s,(w,None)))
			self.next_btn.bind(texture_size=self.next_btn.setter("size"))
			self.add_widget(self.next_btn)
		if(self.now_id != 0):
			self.prev_btn = Button(text="<",font_size=50,background_color=(0,0,0,1),size_hint=(self.trav_width,self.trav_height),pos_hint={"center_x":self.trav_x_prev,"center_y":self.trav_y},valign="center",halign="center",font_name=bold_font,on_press=partial(self.change_photo,self.now_id-1))
			self.prev_btn.bind(width=lambda s,w: s.setter("text_size")(s,(w,None)))
			self.prev_btn.bind(texture_size=self.next_btn.setter("size"))
			self.add_widget(self.prev_btn)

	def add_scroll(self):
		self.start,self.end = self.now_id - self.scroll_nums, self.now_id + self.scroll_nums + 1
		if(self.start<0):
			self.start = 0
		if(self.end>len(self.images)):
			self.end = len(self.images)
		self.play = ScrollView(size_hint=(self.scroll_width, self.scroll_height),pos_hint={"center_x":self.scroll_x,"center_y":self.scroll_y}, size=(Window.width, Window.height))
		self.roll = GridLayout(cols=10000, spacing=10, size_hint_x=None,padding=20)
		self.roll.bind(minimum_width=self.roll.setter('width'))

		self.play.add_widget(self.roll)
		self.add_widget(self.play)

		self.add_scroll_content()

	def add_scroll_content(self):
		self.roll.clear_widgets()
		self.roll.cols = (self.end - self.start)
		for i in range(self.start,self.end):
			this_image = ImageButton(source=self.images[i],size_hint=(None,1.0),on_press=partial(self.change_photo,i))
			self.roll.add_widget(this_image)		

	def change_photo(self,photo_id,_="_"):
		global now_file
		now_file = self.images[photo_id]
		self.on_pre_enter()

	def get_images(self):
		ii = 0
		for file in self.files:
			if(file == now_file):
				self.images.append(file)
				self.now_id = ii
			else:
				this_ext, this_type = get_ext(file)
				if(this_type == self.my_type):
					self.images.append(file)
			ii += 1

	def go_home(self,_="_"):
		self.manager.current = "home_window"

class VideoScreen(Screen):
	def __init__(self,**kwargs):
		super(VideoScreen,self).__init__(**kwargs)
		self.name_width, self.name_height = 0.6,0.08
		self.name_x, self.name_y = 0.5, 0.95
		self.back_width, self.back_height = 0.2, 0.1
		self.back_x, self.back_y = 0.1, 0.95
		self.video_width, self.video_height = 0.9, 0.9
		self.video_x, self.video_y = 0.5, 0.45

	def on_pre_enter(self):
		global now_folder, now_file
		self.clear_widgets()
		self.show_screen()

	def show_screen(self):
		self.add_title()

	def add_title(self):
		global now_file, bold_font
		self.name_label = Label(text=((now_file.split("/"))[-1]),font_size=25,size_hint=(self.name_width,self.name_height),pos_hint={"center_x":self.name_x,"center_y":self.name_y},valign="center",halign="center",font_name=bold_font)
		self.name_label.bind(width=lambda s,w: s.setter("text_size")(s,(w,None)))
		self.name_label.bind(texture_size=self.name_label.setter("size"))
		self.add_widget(self.name_label)
		self.back_btn = Button(text="<-",font_size=50,background_color=(0,0,0,1),size_hint=(self.back_width,self.back_height),pos_hint={"center_x":self.back_x,"center_y":self.back_y},valign="center",halign="center",font_name=bold_font,on_press=self.go_home)
		self.back_btn.bind(width=lambda s,w: s.setter("text_size")(s,(w,None)))
		self.back_btn.bind(texture_size=self.back_btn.setter("size"))
		self.add_widget(self.back_btn)
		self.video = VideoPlayer(source=now_file,state='play',pos_hint={"center_x":self.video_x,"center_y":self.video_y},size_hint=(self.video_width,self.video_height))
		self.add_widget(self.video)
	def go_home(self,_="_"):
		self.clear_widgets()
		self.video.state = "stop"
		self.manager.current = "home_window"

class TextScreen(Screen):
	def __init__(self,**kwargs):
		super(TextScreen,self).__init__(**kwargs)

class MusicScreen(Screen):
	def __init__(self,**kwargs):
		super(MusicScreen,self).__init__(**kwargs)
		self.fold_name_width, self.fold_name_height = 0.6,0.08
		self.fold_name_x, self.fold_name_y = 0.5, 0.95
		self.back_width, self.back_height = 0.2, 0.1
		self.back_x, self.back_y = 0.1, 0.95
		self.name_width, self.name_height = 1.0, 0.13
		self.name_x, self.name_y = 0.5, 0.825
		self.play_width, self.play_height = 0.09, 0.06
		self.play_x, self.play_y = 0.1, 0.7
		self.stop_width, self.stop_height = 0.09, 0.06
		self.stop_x, self.stop_y = 0.2, 0.7
		self.seek_width, self.seek_height = 0.39, 0.06
		self.seek_x, self.seek_y = 0.45, 0.7
		self.time_width, self.time_height = 0.09, 0.06
		self.time_x, self.time_y = 0.7, 0.7
		self.vol_width, self.vol_height = 0.19, 0.06
		self.vol_x, self.vol_y = 0.85, 0.7

	def add_sound(self):
		self.name_label = Label(text=((now_file.split("/"))[-1]),font_size=30,size_hint=(self.name_width,self.name_height),pos_hint={"center_x":self.name_x,"center_y":self.name_y},valign="center",halign="center",font_name=bold_font)
		self.name_label.bind(width=lambda s,w: s.setter("text_size")(s,(w,None)))
		self.name_label.bind(texture_size=self.name_label.setter("size"))
		self.add_widget(self.name_label)
		self.play_btn = Button(text="play",font_size=25,background_color=(0,0,0,1),size_hint=(self.play_width,self.play_height),pos_hint={"center_x":self.play_x,"center_y":self.play_y},valign="center",halign="center",font_name=bold_font,on_press=partial(self.toggle_play,0))
		self.play_btn.bind(width=lambda s,w: s.setter("text_size")(s,(w,None)))
		self.play_btn.bind(texture_size=self.play_btn.setter("size"))
		self.add_widget(self.play_btn)
		self.stop_btn = Button(text="stop",font_size=25,background_color=(0,0,0,1),size_hint=(self.stop_width,self.stop_height),pos_hint={"center_x":self.stop_x,"center_y":self.stop_y},valign="center",halign="center",font_name=bold_font,on_press=partial(self.toggle_play,1))
		self.stop_btn.bind(width=lambda s,w: s.setter("text_size")(s,(w,None)))
		self.stop_btn.bind(texture_size=self.stop_btn.setter("size"))
		self.add_widget(self.stop_btn)
		self.seek = Slider(min=0, max =self.audio_lenght,size_hint=(self.seek_width,self.seek_height),pos_hint={"center_x":self.seek_x,"center_y":self.seek_y},on_press=partial(self.temp_play,0),on_release=partial(self.temp_play,1))
		self.seek.bind(value=self.seek_audio)
		self.add_widget(self.seek)
		self.time_label = Label(text="0:0",font_size=25,size_hint=(self.time_width,self.time_height),pos_hint={"center_x":self.time_x,"center_y":self.time_y},valign="center",halign="center",font_name=bold_font)
		self.time_label.bind(width=lambda s,w: s.setter("text_size")(s,(w,None)))
		self.time_label.bind(texture_size=self.time_label.setter("size"))
		self.add_widget(self.time_label)
		threading.Thread(target=self.time_set).start()
		self.volume = Slider(min=0.0, max =1.0,size_hint=(self.vol_width,self.vol_height),pos_hint={"center_x":self.vol_x,"center_y":self.vol_y})
		self.volume.bind(value=self.vol_audio)
		self.add_widget(self.volume)

	def seek_audio(self, instance, rate):
		if(self.seeking):
			print("###############")
			val_read = int(rate)
			self.audio_file.seek(val_read)
			# time.sleep(1)

	def vol_audio(self, instance, rate):
		self.audio_file.volume = (rate)

	def time_set(self,_="_"):
		while(self.manager.current == "music_player"):
			time_ = int(self.audio_file.get_pos())
			# print(time_)
			# self.seek.value = time_
			time_str = str(time_//60) + ":" + str(time_%60)
			self.time_label.text = time_str

	def seek_set(self,_="_"):
		while(self.audio_play):
			value_ = int(self.audio_file.get_pos())
			self.seek.value = value_
			# print(value_,self.seek.max,self.seek.value)

	def temp_play(self,my_id,_="_"):
		if(my_id==0):
			self.seeking = True
			print(self.seeking,"::::::::")
			self.audio_play = False
		elif(my_id==1):
			self.seeking = False
			self.audio_play = True
			threading.Thread(target=self.seek_set).start()

	def toggle_play(self,do_id,_="_"):
		if(do_id==0):
			self.audio_play = not(self.audio_play)
			if(self.audio_play):
				self.audio_file.play()
				self.play_btn.text = "pause"
				threading.Thread(target=self.seek_set).start()
			else:
				self.audio_file.stop()
				self.play_btn.text = "play"
		elif(do_id==1):
			self.audio_play = False
			self.audio_file.stop()

	def on_pre_enter(self):
		global now_folder, now_file
		self.files = get_files(now_folder,1)
		self.now_id = -1
		self.ext,self.my_type = get_ext(now_file)
		self.audios = []
		self.audio_file = SoundLoader.load(now_file)
		self.audio_lenght = self.audio_file.length
		print(self.audio_lenght,"________________________")
		self.audio_play = False
		self.seeking = True
		# self.get_audios()
		self.clear_widgets()
		self.show_screen()
		threading.Thread(target=self.seek_set).start()

	def show_screen(self):
		self.add_title()
		self.add_sound()

	def add_title(self):
		global now_file, bold_font
		self.fold_name_label = Label(text=((now_file.split("/"))[-2]),font_size=25,size_hint=(self.fold_name_width,self.fold_name_height),pos_hint={"center_x":self.fold_name_x,"center_y":self.fold_name_y},valign="center",halign="center",font_name=bold_font)
		self.fold_name_label.bind(width=lambda s,w: s.setter("text_size")(s,(w,None)))
		self.fold_name_label.bind(texture_size=self.fold_name_label.setter("size"))
		self.add_widget(self.fold_name_label)
		self.back_btn = Button(text="<-",font_size=50,background_color=(0,0,0,1),size_hint=(self.back_width,self.back_height),pos_hint={"center_x":self.back_x,"center_y":self.back_y},valign="center",halign="center",font_name=bold_font,on_press=self.go_home)
		self.back_btn.bind(width=lambda s,w: s.setter("text_size")(s,(w,None)))
		self.back_btn.bind(texture_size=self.back_btn.setter("size"))
		self.add_widget(self.back_btn)

	def get_audios(self):
		ii = 0
		for file in self.files:
			if(file == now_file):
				self.audios.append(file)
				self.now_id = ii
			else:
				this_ext, this_type = get_ext(file)
				if(this_type == self.my_type):
					self.audios.append(file)
			ii += 1

	def go_home(self,_="_"):
		self.audio_file.stop()
		self.manager.current = "home_window"

class MainClass(App):
	def build(self):
		ScreenMan = ScreenManagerbuild()

		ScreenMan.add_widget(HomeScreen(name='home_window'))
		ScreenMan.add_widget(ImageScreen(name='image_viewer'))
		ScreenMan.add_widget(VideoScreen(name='video_player'))
		ScreenMan.add_widget(TextScreen(name='text_editor'))
		ScreenMan.add_widget(MusicScreen(name='music_player'))

		return ScreenMan

class ScreenManagerbuild(ScreenManager):
	pass

if __name__ == '__main__':
	global now_folder, bold_font, curve_font
	now_folder = "/media/nil/NIHAL/Nil/videos/"
	bold_font = "fonts/LobsterTwo-BoldItalic.otf"
	curve_font = "fonts/Arizonia-Regular.ttf"
	file_exts = json_loader("exts.json")
	MainClass().run()

