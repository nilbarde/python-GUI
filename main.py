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
import threading

from gtts import gTTS 

class HomeScreen(Screen):
	def __init__(self,**kwargs):
		super(HomeScreen,self).__init__(**kwargs)
		self.scroll_width, self.scroll_height = 1.0,1.0
		self.scroll_x, self.scroll_y = 0.5, 0.5
		self.mytext = "It's Nihal Barde"
		self.language = 'en'
		self.save_path = "text_speech.mp3"

	def on_pre_enter(self):
		self.clear_widgets()
		self.add_scroll()
		self.convert_speech()

	def add_scroll(self):
		self.play = ScrollView(size_hint=(self.scroll_width, self.scroll_height),pos_hint={"center_x":self.scroll_x,"center_y":self.scroll_y}, size=(Window.width, Window.height))
		self.roll = GridLayout(cols=1,spacing=5, size_hint_y=None,padding=10)
		self.roll.bind(minimum_height=self.roll.setter('height'))
		self.play.add_widget(self.roll)
		self.add_widget(self.play)		

		self.textinput = TextInput(font_size = 20)

	def convert_speech(self):
		myobj = gTTS(text=self.mytext, lang=self.language, slow=False)
		myobj.save(self.save_path)

	def read_speech(self):
		self.audio_file = SoundLoader.load(self.save_path)
		self.audio_lenght = self.audio_file.length
		print(self.audio_lenght,"________________________")
		self.audio_play = False
		self.audio_file.play()
		self.play_btn.text = "pause"


class MainClass(App):
	def build(self):
		ScreenMan = ScreenManagerbuild()

		ScreenMan.add_widget(HomeScreen(name='home_window'))

		return ScreenMan

class ScreenManagerbuild(ScreenManager):
	pass

myobj = gTTS(text="nihal plays football", lang="en", slow=False)
myobj.save("sound.mp3")
if __name__ == '__main__':
	MainClass().run()

