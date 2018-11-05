import kivy

from kivy.app import App

from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.uix.progressbar import ProgressBar
from kivy.uix.image import Image, AsyncImage

from functools import partial
import time

from pytube import YouTube
import moviepy.editor as mpe

from os import walk,path,makedirs,rename
import threading

from os.path import dirname as os_dirname
from os.path import exists as os_exists
from os import makedirs as os_makedirs

def ensure_dir(file_path):
	if '/' in file_path:
		directory = os_dirname(file_path)
		if not os_exists(directory):
			os_makedirs(directory)


class HomeScreen(Screen):
	def __init__(self,**kwargs):
		super(HomeScreen,self).__init__(**kwargs)
		self.logo_width, self.logo_height = 0.6, 0.08
		self.logo_x, self.logo_y = 0.5, 0.95
		self.searchbox_width, self.searchbox_height = 0.58, 0.07
		self.searchbox_x, self.searchbox_y = 0.4, 0.85
		self.searchbtn_width, self.searchbtn_height = 0.18, 0.07
		self.searchbtn_x, self.searchbtn_y = 0.8, 0.85
		self.scroll_width, self.scroll_height = 0.98, 0.78
		self.scroll_x, self.scroll_y = 0.5, 0.4

	def on_pre_enter(self):
		self.clear_widgets()
		self.show_title()
		self.add_scroll()

	def show_title(self):
		self.logo = Button(text="Youtube Downloader",font_size=60,background_color=(0,0,0,1),halign='center',valign='center',size_hint=(self.logo_width,self.logo_height),pos_hint={"center_x":self.logo_x,"center_y":self.logo_y},font_name=font_names["Arizonia"],on_press=self.go_home)
		self.add_widget(self.logo)
		self.searchbox = TextInput(font_size=20,font_name=font_names["LobsterTwo-Bold"],size_hint=(self.searchbox_width,self.searchbox_height),pos_hint={"center_x":self.searchbox_x,"center_y":self.searchbox_y})
		self.add_widget(self.searchbox)
		search_btn = Button(text="Search",font_size=20,valign="center",halign="center",size_hint=(self.searchbtn_width,self.searchbtn_height),pos_hint={"center_x":self.searchbtn_x,"center_y":self.searchbtn_y},font_name=font_names["LobsterTwo-Bold"],on_press=self.go_search)
		search_btn.bind(width=lambda s,w: s.setter("text_size")(s,(w,None)))
		search_btn.bind(texture_size=search_btn.setter("size"))
		self.add_widget(search_btn)

	def add_scroll(self):
		self.play = ScrollView(size_hint=(self.scroll_width, self.scroll_height),pos_hint={"center_x":self.scroll_x,"center_y":self.scroll_y}, size=(Window.width, Window.height))
		self.roll = GridLayout(cols=1,spacing=5,size_hint_y=None,padding=10)
		self.roll.bind(minimum_height=self.roll.setter('height'))

		self.play.add_widget(self.roll)
		self.add_widget(self.play)

	def go_search(self, _="_"):
		self.roll.clear_widgets()
		link = (self.searchbox.text)
		self.fetch_data = YouTube(link)
		self.mp4_videos = self.fetch_data.streams.filter(file_extension='mp4').all()
		self.thumbnail = AsyncImage(source=self.fetch_data.thumbnail_url,height=200,size_hint=(0.2,None),keep_ratio=True,allow_stretch=True)
		self.roll.add_widget(self.thumbnail)
		self.video_name = Label(text=self.fetch_data.title,font_size=30,valign="center",halign="center",size_hint_y=None,size_hint_x=0.8,font_name=font_names["LobsterTwo-Bold"])
		self.video_name.bind(width=lambda s,w: s.setter("text_size")(s,(w,None)))
		self.roll.add_widget(self.video_name)
		for video in self.mp4_videos:
			print(video)
			res = video.resolution
			self.res_name = Button(text=str(res),font_size=30,valign="center",halign="center",size_hint_y=None,font_name=font_names["LobsterTwo-Bold"],on_press=partial(self.download,video))
			self.res_name.bind(width=lambda s,w: s.setter("text_size")(s,(w,None)))
			self.roll.add_widget(self.res_name)

	def download(self,video,_="_"):
		global down_video, link_data 
		link_data = self.fetch_data
		down_video = video
		self.manager.current = "down_window"

	def go_home(self,_="_"):
		self.manager.current = "home_window"

class DownScreen(Screen):
	def __init__(self,**kwargs):
		super(DownScreen,self).__init__(**kwargs)
		global down_video, link_data
		self.logo_width, self.logo_height = 0.6, 0.08
		self.logo_x, self.logo_y = 0.5, 0.95
		self.name_width, self.name_height = 0.5, 0.08
		self.name_x, self.name_y = 0.5, 0.85
		self.title_width, self.title_height = 0.8, 0.08
		self.title_x, self.title_y = 0.5, 0.75
		self.progtext_width, self.progtext_height = 0.3, 0.08
		self.progtext_x, self.progtext_y = 0.5, 0.55
		self.progress_width, self.progress_height = 0.8, 0.08
		self.progress_x, self.progress_y = 0.5, 0.45
		self.status_width, self.status_height = 0.8, 0.08
		self.status_x, self.status_y = 0.5, 0.3

	def on_pre_enter(self):
		global down_video, link_data
		self.clear_widgets()
		self.percentage = 0.0
		self.progress_callback=self.update_progress_bar
		link_data.register_on_progress_callback(self.progress_callback)
		self.file_size = down_video.filesize
		self.status_text = "Downloading"
		self.show_title()
		threading.Thread(target=self.download_video).start()
		# self.download_video()

	def show_title(self):
		global down_video, link_data
		self.logo = Button(text="Youtube Downloader",font_size=60,background_color=(0,0,0,1),halign='center',valign='center',size_hint=(self.logo_width,self.logo_height),pos_hint={"center_x":self.logo_x,"center_y":self.logo_y},font_name=font_names["Arizonia"],on_press=self.go_home)
		self.logo.bind(width=lambda s,w: s.setter("text_size")(s,(w,None)))
		self.logo.bind(texture_size=self.logo.setter("size"))
		self.add_widget(self.logo)
		print(link_data.title,type(link_data.title),"____________________")
		self.name_ = Label(text=str(link_data.title),font_size=40,halign='center',valign='center',size_hint=(self.name_width,self.name_height),pos_hint={"center_x":self.name_x,"center_y":self.name_y},font_name=font_names["Arizonia"])
		self.name_.bind(width=lambda s,w: s.setter("text_size")(s,(w,None)))
		self.name_.bind(texture_size=self.name_.setter("size"))
		self.add_widget(self.name_)
		self.title_lbl = Label(text=down_video.default_filename + " (" + down_video.resolution + ") ",font_size=40,halign='center',valign='center',size_hint=(self.title_width,self.title_height),pos_hint={"center_x":self.title_x,"center_y":self.title_y},font_name=font_names["LobsterTwo-Bold"])
		self.title_lbl.bind(width=lambda s,w: s.setter("text_size")(s,(w,None)))
		self.title_lbl.bind(texture_size=self.title_lbl.setter("size"))
		self.add_widget(self.title_lbl)
		self.progressbar = ProgressBar(max=100,size_hint=(self.progress_width,self.progress_height),pos_hint={"center_x":self.progress_x,"center_y":self.progress_y})
		self.add_widget(self.progressbar)
		self.progtext = Label(text=str(self.percentage),font_size=40,halign='center',valign='center',size_hint=(self.progtext_width,self.progtext_height),pos_hint={"center_x":self.progtext_x,"center_y":self.progtext_y},font_name=font_names["LobsterTwo-Bold"])
		self.progtext.bind(width=lambda s,w: s.setter("text_size")(s,(w,None)))
		self.progtext.bind(texture_size=self.progtext.setter("size"))
		self.add_widget(self.progtext)
		self.status = Label(text=str(self.status_text),font_size=40,halign='center',valign='center',size_hint=(self.status_width,self.status_height),pos_hint={"center_x":self.status_x,"center_y":self.status_y},font_name=font_names["LobsterTwo-Bold"])
		self.status.bind(width=lambda s,w: s.setter("text_size")(s,(w,None)))
		self.status.bind(texture_size=self.status.setter("size"))
		self.add_widget(self.status)

	def go_home(self,_="_"):
		self.manager.current = "home_window"

	def update_progress_bar(self, stream, chunk, file_handle, bytes_remaining):
		self.percentage = round(((self.file_size - bytes_remaining) / self.file_size) * 100,2)
		self.progressbar.value = self.percentage
		self.progtext.text = str(self.percentage)

	def download_video(self):
		global down_video, link_data

		audio_videos = link_data.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().all()

		if(down_video in audio_videos):
			print("starting downloading of video")
			start = time.time()
			self.status_text = "Downloading Video"
			self.status.text = self.status_text
			down_video.download("downloads/")
			self.status_text = "Video Downloaded Successfully"
			self.status.text = self.status_text
			end = time.time()
			print("downloaded video " + down_video.default_filename + " in " + str(end-start) + " secs")
			# self.go_home()
		else:
			print("need to download audio and video differently")
			video_fold = "downloads/videos/"
			start = time.time()
			self.status_text = "Downloading Video"
			self.status.text = self.status_text
			down_video.download(video_fold)
			end = time.time()
			print("video file downloaded in " + str(end-start) + " secs")
			video_title = down_video.default_filename
			audios = link_data.streams.filter(only_audio=True).order_by('abr').all()
			audio_fold = "downloads/audios/"
			self.status_text = "Downloading Audio"
			self.status.text = self.status_text
			audios[-1].download(audio_fold)
			end = time.time()
			print("audio file downloaded in " + str(end-start) + " secs")
			audio_title = audios[-1].default_filename
			audio_path = self.rename_me(audio_fold + audio_title)
			print(audio_title)
			self.status_text = "Loading Video"
			self.status.text = self.status_text
			my_clip = mpe.VideoFileClip(video_fold + video_title)
			print("loaded video")
			self.status_text = "Loading Audio"
			self.status.text = self.status_text
			audio_clip = mpe.AudioFileClip(audio_path)
			print("loaded audio")
			final_clip = my_clip.set_audio(audio_clip)
			print("added audio in video")
			self.status_text = "Writing Video"
			self.status.text = self.status_text
			final_clip.write_videofile("downloads/"+video_title)
			end = time.time()
			print("downloaded video " + down_video.default_filename + " in " + str(end-start) + " secs")
			self.status_text = "Video Downloaded Successfully"
			self.status.text = self.status_text
			# self.go_home()

	def rename_me(self,name):
		deep = 1
		found_ext = False
		ext = ""
		print(name)
		while not(found_ext):
			print(deep)
			print(name[-deep])
			if(name[-deep]=="."):
				ext = name[-deep+1:]
				found_ext = True
			deep += 1
		new_name = name[:-len(ext)] + "mp3"
		rename(name,new_name)
		return new_name

class MainClass(App):
	def build(self):
		ScreenMan = ScreenManagerbuild()

		ScreenMan.add_widget(HomeScreen(name='home_window'))
		ScreenMan.add_widget(DownScreen(name='down_window'))
		
		return ScreenMan

class ScreenManagerbuild(ScreenManager):
	pass

if __name__ == '__main__':
	global downloaded_details,font_names,down_mode, link, now_cat, show_details
	font_names = {}
	ensure_dir("downloads/videos/")
	ensure_dir("downloads/audios/")
	font_names["LobsterTwo-Bold"] = "fonts/LobsterTwo-Bold.otf"
	font_names["Arizonia"] = "fonts/Arizonia-Regular.ttf"
	MainClass().run()
