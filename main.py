import kivy

from kivy.app import App

from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.button import Button
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.label import Label
from kivy.uix.checkbox import CheckBox
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget

from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window

from kivy.uix.image import Image
from kivy.uix.videoplayer import VideoPlayer
from kivy.graphics import Color, Ellipse, Rectangle, RoundedRectangle

from kivy.properties import StringProperty,BooleanProperty
from kivy.uix.slider import Slider
from kivy.uix.popup import Popup

from functools import partial
from random import shuffle, randint, choice
from datetime import datetime

from os import makedirs
from os.path import exists,dirname,isfile
from json_funs import *
from os_funs import *

import cv2
import numpy as np
import threading
from os import remove

def EnText(line,code=0):
	KeyEnc = [i for i in CodeDict[code] if i<128]

	NewLine = ""
	for i in range(len(line)):
		RotateKey = i%(len(KeyEnc))
		NowEnc = KeyEnc[RotateKey:] + KeyEnc[:RotateKey]
		# NowEnc = KeyEnc

		Num = ord(line[i])
		NewLine += chr(NowEnc[Num])
	return NewLine

def DeText(line,code=0):
	KeyEnc = [i for i in CodeDict[code] if i<128]
	KeyDec = [0 for i in range(len(KeyEnc))]
	NewLine = ""
	for i in range(len(line)):
		RotateKey = i%(len(KeyEnc))
		NowEnc = KeyEnc[RotateKey:] + KeyEnc[:RotateKey]
		for j in range(len(NowEnc)):
			KeyDec[NowEnc[j]] = j
		Num = ord(line[i])
		NewLine += chr(KeyDec[Num])
	return NewLine

def EnImage(img,code):
	# global en_color
	# global d_en_color
	en_color = {}
	for i in range(len(CodeDict[code])):
		en_color[i] = CodeDict[code][i]
	img.astype('int16')
	img = np.vectorize(en_color.get, otypes=[np.float])(img)
	img_shape = img.shape
	img_add = np.arange(img.size).reshape(img.shape)
	img_add = img_add%256
	img_add = np.vectorize(en_color.get, otypes=[np.float])(img_add)
	img = img + img_add
	img%=256
	img.astype('uint8')
	return img

def DeImage(img,code):
	en_color = {}
	for i in range(len(CodeDict[code])):
		en_color[i] = CodeDict[code][i]
	d_en_color = {}
	for i in range(len(CodeDict[code])):
		d_en_color[CodeDict[code][i]] = i
	global d_en_color
	img.astype('int16')
	img_add = np.arange(img.size).reshape(img.shape)
	img_add = img_add%256
	img_add = np.vectorize(en_color.get, otypes=[np.float])(img_add)
	img = img-img_add
	img = img%256
	img = np.vectorize(d_en_color.get, otypes=[np.float])(img)
	img.astype('uint8')
	return img

class ImageButton(ButtonBehavior, Image):
	pass

class LockScreen(Screen):
	def __init__(self,**kwargs):
		super(LockScreen,self).__init__(**kwargs)
		self.PasswordLength = 4
		self.DefineLayout()

	def _keyboard_closed(self):
		self._keyboard.unbind(on_key_down=self._on_keyboard_down)
		self._keyboard = None

	def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
		# Reading Keyboard Inputs
		key_no, self.pressed_key = keycode
		self.KeyPressed(self.pressed_key)

	def DefineLayout(self):
		self.DefineKeyPadLayout()
		self.DefineShowLayout()
		self.DefineModeLayout()

	def DefineKeyPadLayout(self):
		self.KeyPadW, self.KeyPadH = 0.4, 0.7
		self.KeyPadX, self.KeyPadY = 0.5, 0.4

		self.KeyPadKeys  = [str(i) for i in range(1,10)]
		self.KeyPadKeys += ["c","0","<-"]
		self.KeyMeanings = {}
		for i in range(10):
			self.KeyMeanings[str(i)] = i
			self.KeyMeanings["numpad" + str(i)] = i

	def DefineShowLayout(self):
		self.ShowPadW, self.ShowPadH = 0.4, 0.15
		self.ShowPadX, self.ShowPadY = 0.5, 0.875

	def DefineModeLayout(self):
		self.ModeW, self.ModeH = [0.3, 0.3], [0.15, 0.15]
		self.ModeX, self.ModeY = [0.15, 0.85], [0.875, 0.875]
		self.BackW, self.BackH = [0.3, 0.3], [0.15, 0.15]
		self.BackX, self.BackY = [0.15, 0.85], [0.125, 0.125]

	def on_pre_enter(self):
		self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
		self._keyboard.bind(on_key_down=self._on_keyboard_down)

		self.KeysEntered = 0
		self.cust_pre_enter()

	def cust_pre_enter(self):
		self.clear_widgets()
		global mode
		for i in range(len(self.ModeX)):
			self.add_widget(Label(text=mode,font_size=30,halign='center',valign='center',font_name=FontDict["LobsterTwo-BoldItalic"],size_hint=(self.ModeW[i],self.ModeH[i]),pos_hint={"center_x":self.ModeX[i],"center_y":self.ModeY[i]}))
			if(mode=="password"):
				self.add_widget(Button(text="Go Back",background_color=(0.5,0.5,0.5,0.5),font_size=30,halign='center',valign='center',font_name=FontDict["LobsterTwo-BoldItalic"],size_hint=(self.BackW[i],self.BackH[i]),pos_hint={"center_x":self.BackX[i],"center_y":self.BackY[i]},on_press=self.GoBack))
		self.KeyPad = GridLayout(cols=3,spacing=5,padding=5,size_hint=(self.KeyPadW,self.KeyPadH),pos_hint={"center_x":self.KeyPadX,"center_y":self.KeyPadY})
		self.add_widget(self.KeyPad)
		self.AddKeys()
		self.ShowPad = GridLayout(cols=self.PasswordLength,spacing=5,padding=5,size_hint=(self.ShowPadW,self.ShowPadH),pos_hint={"center_x":self.ShowPadX,"center_y":self.ShowPadY})
		self.add_widget(self.ShowPad)
		self.AddShowPad()

	def AddKeys(self):
		for Key in self.KeyPadKeys:
			Btn = Button(text=Key,font_size=30,background_color=(0.5,0.5,0.5,1),halign='center',valign='center',font_name=FontDict["LobsterTwo-BoldItalic"],on_press=partial(self.KeyPressed,Key))
			self.KeyPad.add_widget(Btn)

	def AddShowPad(self):
		self.ShowPadKeys = {}
		for i in range(self.PasswordLength):
			self.ShowPadKeys[i] = {}
			self.ShowPadKeys[i]["button"] = Button(text="-",font_size=30,background_color=(0.5,0.5,0.5,0.5),halign='center',valign='center',font_name=FontDict["LobsterTwo-BoldItalic"])
			self.ShowPadKeys[i]["value"] = None
			self.ShowPad.add_widget(self.ShowPadKeys[i]["button"])

	def KeyPressed(self,Key,_="_"):
		if Key in self.KeyMeanings:
			if(self.KeysEntered<self.PasswordLength):
				self.ShowPadKeys[self.KeysEntered]["button"].text = "*"
				self.ShowPadKeys[self.KeysEntered]["value"] = self.KeyMeanings[Key]
				self.KeysEntered += 1
		elif(Key == self.KeyPadKeys[-3]):
			self.KeysEntered = 0
			for i in range(len(self.ShowPadKeys)):
				self.ShowPadKeys[i]["button"].text = "-"
				self.ShowPadKeys[i]["value"] = None			
		elif((Key == "backspace" or Key == self.KeyPadKeys[-1])  and self.KeysEntered):
			self.KeysEntered -= 1
			self.ShowPadKeys[self.KeysEntered]["button"].text = "-"
			self.ShowPadKeys[self.KeysEntered]["value"] = None
		elif(Key == "enter" and self.KeysEntered==self.PasswordLength):
			NumEntered = ""
			for i in range(self.PasswordLength):
				NumEntered += str(self.ShowPadKeys[i]["value"])
			global mode, password, EnKey
			if(mode=="EnKey"):
				EnKey = int(NumEntered)
				mode = "password"
				self.on_pre_enter()
			elif(mode=="password"):
				if(EnText(NumEntered,EnKey)==UserInfo["password"]):
					self.manager.current = "HomeWindow"
		else:
			print(Key,"meaning not found")

	def GoBack(self,_="_"):
		global mode
		mode = "EnKey"
		self.on_pre_enter()

class HomeScreen(Screen):
	def __init__(self,**kwargs):
		super(HomeScreen,self).__init__(**kwargs)
		self.DefineFolders()
		self.DefineLayout()

	def DefineFolders(self):
		self.EnFold = "./en fold/"
		self.RawFold = "./raw fold/"

	def DefineLayout(self):
		self.ShowW, self.ShowH = 0.6, 0.2
		self.ShowX, self.ShowY = 0.5, 0.65
		self.AddW, self.AddH = 0.6, 0.2
		self.AddX, self.AddY = 0.5, 0.35

	def on_pre_enter(self):
		self.clear_widgets()
		self.cust_pre_enter()

	def cust_pre_enter(self):
		folders = get_folders(self.RawFold)
		self.NewFiles = get_files(self.RawFold,[".jpg",".png"],False)
		for folder in folders:
			self.NewFiles += get_files(folder,[".jpg",".png"],True)
		self.EnFiles = get_files(self.EnFold,[".jpg",".png"],False)
		self.ShowButtons()

	def ShowButtons(self):
		ShowBtn = Button(text = "Show (" + str(len(UserInfo["images"])) + ")" ,font_size=45,background_color=(0.5,0.5,0.5,0.5),size_hint=(self.ShowW,self.ShowH),pos_hint={"center_x":self.ShowX,"center_y":self.ShowY},valign="center",halign="center",font_name=FontDict["LobsterTwo-BoldItalic"],on_press=self.ShowImages)
		self.add_widget(ShowBtn)
		AddBtn = Button(text="Add (" + str(len(self.NewFiles)) + ")" ,font_size=45,background_color=(0.5,0.5,0.5,0.5),size_hint=(self.AddW,self.AddH),pos_hint={"center_x":self.AddX,"center_y":self.AddY},valign="center",halign="center",font_name=FontDict["LobsterTwo-BoldItalic"],on_press=self.AddImages)
		self.add_widget(AddBtn)

	def AddImages(self,_="_"):
		self.manager.current = "AddWindow"

	def ShowImages(self,_="_"):
		self.manager.current = "ShowWindow"

class AddScreen(Screen):
	def __init__(self,**kwargs):
		super(AddScreen,self).__init__(**kwargs)
		self.DefineFolders()
		self.DefineLayout()

	def DefineFolders(self):
		self.EnFold = "./en fold/"
		self.RawFold = "./raw fold/"

	def DefineLayout(self):
		self.ShowW, self.ShowH = 0.6, 0.2
		self.ShowX, self.ShowY = 0.5, 0.65
		self.ProgressW, self.ProgressH = 0.6, 0.2
		self.ProgressX, self.ProgressY = 0.5, 0.35

	def on_pre_enter(self):
		self.AddedImages = 0
		self.cust_pre_enter()

	def cust_pre_enter(self):
		folders = get_folders(self.RawFold)
		self.NewFiles = get_files(self.RawFold,[".jpg",".png"],True)
		for folder in folders:
			self.NewFiles += get_files(folder,[".jpg",".png"],True)
		self.EnFiles = get_files(self.EnFold,[".jpg",".png"],False)
		self.ShowLabels()
		threading.Thread(target=self.AddImages).start()

	def ShowLabels(self):
		ShowBtn = Label(text = "Adding " + str(len(self.NewFiles)) + " images" ,font_size=45,background_color=(0.5,0.5,0.5,0.5),size_hint=(self.ShowW,self.ShowH),pos_hint={"center_x":self.ShowX,"center_y":self.ShowY},valign="center",halign="center",font_name=FontDict["LobsterTwo-BoldItalic"])
		self.add_widget(ShowBtn)

		self.ProgressBtn = Label(text = str((self.AddedImages)) + " images added" ,font_size=45,background_color=(0.5,0.5,0.5,0.5),size_hint=(self.ProgressW,self.ProgressH),pos_hint={"center_x":self.ProgressX,"center_y":self.ProgressY},valign="center",halign="center",font_name=FontDict["LobsterTwo-BoldItalic"])
		self.add_widget(self.ProgressBtn)

	def AddImages(self):
		for RawImageName in self.NewFiles:
			global EnKey
			EnImageName = str(len(UserInfo["images"])+1) + ".png"
			UserInfo["images"][EnImageName[:-4]] = EnText(RawImageName[:-4],EnKey) + RawImageName[-4:]
			RawImage = cv2.imread(RawImageName)
			global EnKey
			MyEnImage = EnImage(RawImage,EnKey)
			cv2.imwrite(self.EnFold + EnImageName,MyEnImage)
			self.AddedImages += 1
			self.ProgressBtn.text = str((self.AddedImages)) + " images added"
			write_json(UserInfo,"./info/info.json")
		self.manager.current = "HomeWindow"

class ShowScreen(Screen):
	def __init__(self,**kwargs):
		super(ShowScreen,self).__init__(**kwargs)
		self.DefineFolders()
		self.DefineLayout()

	def _keyboard_show_closed(self):
		self._keyboard_show.unbind(on_key_down=self._on_keyboard_show_down)
		self._keyboard_show = None

	def _on_keyboard_show_down(self, keyboard, keycode, text, modifiers):
		# Reading Keyboard Inputs
		key_no, self.pressed_key = keycode
		if(self.pressed_key=="right" or self.pressed_key=="up"):
			self.ChangeImage(self.NowImage + 1)
		elif(self.pressed_key=="left" or self.pressed_key=="down"):
			self.ChangeImage(self.NowImage - 1)

	def DefineFolders(self):
		self.EnFold = "./en fold/"
		self.RawFold = "./raw fold/"

	def DefineLayout(self):
		self.ShowW, self.ShowH = 0.6, 0.1
		self.ShowX, self.ShowY = 0.5, 0.95
		self.ImageW, self.ImageH = 0.89, 0.89
		self.ImageX, self.ImageY = 0.5, 0.45

		self.PrevW, self.PrevH = 0.05, 0.9
		self.PrevX, self.PrevY = 0.025, 0.45
		self.NextW, self.NextH = 0.05, 0.9
		self.NextX, self.NextY = 0.975, 0.45

		self.HomeW, self.HomeH = [0.2, 0.2], [0.1, 0.1]
		self.HomeX, self.HomeY = [0.1, 0.9], [0.95, 0.95]

	def on_pre_enter(self):
		self._keyboard_show = Window.request_keyboard(self._keyboard_show_closed, self)
		self._keyboard_show.bind(on_key_down=self._on_keyboard_show_down)
		self.NowImage = 1
		self.cust_pre_enter()

	def cust_pre_enter(self):
		self.clear_widgets()
		self.TotImages = len(UserInfo["images"])
		self.ShowLabels()
		MyEnImage = cv2.imread(self.EnFold + str(self.NowImage) + ".png")
		MyDeImage = DeImage(MyEnImage,EnKey)
		cv2.imwrite(self.EnFold + "0.png",MyDeImage)
		self.ShowImages()

	def ShowLabels(self):
		global EnKey
		text = DeText(UserInfo["images"][str(self.NowImage)][:-4],EnKey) + UserInfo["images"][str(self.NowImage)][-4:]
		ShowBtn = Label(text = text ,font_size=45,background_color=(0.5,0.5,0.5,0.5),size_hint=(self.ShowW,self.ShowH),pos_hint={"center_x":self.ShowX,"center_y":self.ShowY},valign="center",halign="center",font_name=FontDict["LobsterTwo-BoldItalic"])
		self.add_widget(ShowBtn)
		for i in range(len(self.HomeW)):
			self.add_widget(Button(text="Go Home",background_color=(0.5,0.5,0.5,0.5),font_size=30,halign='center',valign='center',font_name=FontDict["LobsterTwo-BoldItalic"],size_hint=(self.HomeW[i],self.HomeH[i]),pos_hint={"center_x":self.HomeX[i],"center_y":self.HomeY[i]},on_press=self.GoHome))

	def ShowImages(self):
		self.ImageGrid = GridLayout(cols=1,size_hint=(self.ImageW,self.ImageH),pos_hint={"center_x":self.ImageX,"center_y":self.ImageY})
		self.ShowImage = ImageButton(source=self.EnFold + "0.png",allow_stretch=True,keep_ratio=True)
		self.ShowImage.reload()
		self.ImageGrid.add_widget(self.ShowImage)
		self.add_widget(self.ImageGrid)
		if(self.NowImage>1):
			PrevBtn = Button(text = "<" ,font_size=45,background_color=(0.5,0.5,0.5,0.5),size_hint=(self.PrevW,self.PrevH),pos_hint={"center_x":self.PrevX,"center_y":self.PrevY},valign="center",halign="center",font_name=FontDict["LobsterTwo-BoldItalic"],on_press=partial(self.ChangeImage,self.NowImage-1))
			self.add_widget(PrevBtn)
		if(self.NowImage<self.TotImages):
			NextBtn = Button(text = ">" ,font_size=45,background_color=(0.5,0.5,0.5,0.5),size_hint=(self.NextW,self.NextH),pos_hint={"center_x":self.NextX,"center_y":self.NextY},valign="center",halign="center",font_name=FontDict["LobsterTwo-BoldItalic"],on_press=partial(self.ChangeImage,self.NowImage+1))
			self.add_widget(NextBtn)

	def ChangeImage(self,ImageNum,_="_"):
		self.NowImage = ImageNum
		self.cust_pre_enter()

	def GoHome(self,_="_"):
		self.manager.current = "HomeWindow"

class MainClass(App):
	def build(self):
		ScreenMan = ScreenManagerbuild()

		ScreenMan.add_widget(LockScreen(name='LockWindow'))

		ScreenMan.add_widget(HomeScreen(name='HomeWindow'))

		ScreenMan.add_widget(ShowScreen(name='ShowWindow'))
		ScreenMan.add_widget(AddScreen(name='AddWindow'))

		return ScreenMan

class ScreenManagerbuild(ScreenManager):
	pass

if __name__ == '__main__':
	global mode, password, EnKey
	mode = "EnKey"
	password = "none"
	EnKey = 0
	CodeDict = []
	for i in range(10):
		CodeDict += read_json("./info/codes/codes_" + str(i+1) + ".json")
	FontDict = read_json("./info/fonts.json")
	UserInfo = read_json("./info/info.json")
	try:
		MainClass().run()
	except:
		pass
	try:
		remove("./en fold/0.png")
	except:
		pass
