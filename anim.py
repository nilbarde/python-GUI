try:
	import kivy

	from kivy.app import App

	from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
	from kivy.uix.button import Button
	from kivy.uix.behaviors import ButtonBehavior
	from kivy.uix.label import Label
	from kivy.uix.checkbox import CheckBox
	from kivy.uix.textinput import TextInput
	from kivy.uix.widget import Widget
	from kivy.clock import Clock
	from kivy.animation import Animation

	from kivy.uix.gridlayout import GridLayout
	from kivy.uix.boxlayout import BoxLayout
	from kivy.uix.floatlayout import FloatLayout
	from kivy.uix.scrollview import ScrollView
	from kivy.core.window import Window

	from kivy.uix.image import Image
	from kivy.uix.videoplayer import VideoPlayer
	from kivy.graphics import Color, Ellipse, Rectangle, RoundedRectangle

	from kivy.properties import StringProperty,BooleanProperty, ListProperty
	from kivy.uix.slider import Slider
	from kivy.uix.popup import Popup

	from functools import partial
	from random import shuffle, randint, choice, sample
	from datetime import datetime

	from os import makedirs
	from os.path import exists,dirname,isfile
	from json_funs import *
	import time
	from time import sleep

except:
	print("*******************************")
	print("  error in importing packages  ")
	print("*******************************")

def LoadDict():
	global MainDict, AppImages, FontDict
	MainDict = read_json("./data/accounts.json")
	AppImages = read_json("./data/app_images.json")
	FontDict = read_json("/home/nil/Nil/My Codes/github/fonts/fonts.json")

def SaveDict():
	global MainDict, AppImages, FontDict
	write_json(MainDict,"./data/accounts.json")
	write_json(AppImages,"./data/app_images.json")

class ImageButton(ButtonBehavior, Image):
	pass

class HomeScreen(Screen):
	def __init__(self,**kwargs):
		super(HomeScreen,self).__init__(**kwargs)
		self.LastWindow = "Home"
		self.NowWindow = "Home"
		self.MenuOpen = False
		self.MouseClickBuffer = 0.01
		self.DefineView()
		self.define_colors()
		# Window.clearcolor = (1,1,1,1)
		# self.AddToggleBtn()
		# self.on_pre_enter()

	def DefineView(self):
		self.TogBtnW, self.TogBtnH = 0.095, 0.095
		self.TogBtnX, self.TogBtnY = 0.05, 0.95

		self.MenuScrollW, self.MenuScrollH = 0.395, 0.995
		self.MenuScrollX, self.MenuScrollY = 0.2, 0.5
		self.MenuHideScrollX, self.MenuHideScrollY = -0.2, 0.5

		self.MainScrollW, self.MainScrollH = 0.99, 0.89
		self.MainScrollX, self.MainScrollY = 0.5, 0.45

	def define_colors(self):
		self.black = (0,0,0,1.0)
		self.white = (1.0,1.0,1.0,1.0)
		self.dark_red = (1.0,0,0,1.0)
		self.dark_green = (0,1.0,0,1.0)
		self.dark_blue = (0,0,1.0,1.0)
		self.red = (0.66,0,0,1.0)
		self.green = (0,0.66,0,1.0)
		self.blue = (0,0,0.66,1.0)
		self.dark_gray = (0.2,0.2,0.2,1.0)
		self.gray = (0.6,0.6,0.6,1.0)
		self.aqua = (0,1.0,1.0,1.0)
		self.magenta = (1.0,0,1.0,1.0)
		self.olive = (0.5,0.5,0,1.0)
		self.purple = (0.5,0,0.5,1.0)
		self.teal = (0,0.5,0.5,1.0)
		self.orange = (0.5,0.6,0,1.0)
		self.all_colors = [self.red,self.green,self.blue,self.gray,self.aqua,self.magenta,self.olive,self.purple,self.teal,self.orange]
		self.all_colors = [self.dark_red,self.red,self.dark_blue,self.blue,self.dark_green,self.green,self.dark_gray,self.gray,
		self.black,self.white,self.aqua,self.magenta,self.olive,self.purple,self.teal,self.orange]

	def on_touch_down(self,touch):
		#On mouse click 
		self.MouseClickX = ((touch.spos[0]))
		self.MouseClickY = ((touch.spos[1]))
		if(self.MenuOpen):
			if(self.MouseClickX>self.MenuScrollW+self.MouseClickBuffer):
				self.ChangeWindow(self.NowWindow)
				self.MenuOpen = False
		super(HomeScreen, self).on_touch_down(touch)	

	def on_pre_enter(self):
		if self.NowWindow == "Home":
			self.clear_widgets()
			Window.clearcolor = (1,1,1,1)
			self.AddToggleBtn()
		elif self.NowWindow == "Menu":
			if self.LastWindow == "Home":
				self.ShowMenu()
			else:
				self.ShowMenu()
		elif self.NowWindow == "ShowCategory":
			self.clear_widgets()
			self.AddToggleBtn()
			self.ShowCategories()
		elif self.NowWindow == "ShowAccount":
			self.clear_widgets()
			self.AddToggleBtn()
			self.ShowAccounts()

	def AddToggleBtn(self,_="_"):
		fun = partial(self.ChangeWindow,"Menu")
		self.TogBtn = ImageButton(source=AppImages["menu"],allow_stretch=True,keep_ratio=True,size_hint=(self.TogBtnW,self.TogBtnH),pos_hint={"center_x":self.TogBtnX,"center_y":self.TogBtnY},on_press=fun)
		self.add_widget(self.TogBtn)
		# self.TransitionBtn()

	############### Menu ###############
	def ShowMenu(self,_="_"):
		self.MenuScrollPlay = ScrollView(size_hint=(self.MenuScrollW, self.MenuScrollH),pos_hint={"center_x":self.MenuHideScrollX,"center_y":self.MenuHideScrollY}, size=(Window.width, Window.height))
		self.MenuScrollRoll = GridLayout(cols=1, spacing=1, size_hint_y=None,padding=1)
		self.MenuScrollRoll.bind(minimum_height=self.MenuScrollRoll.setter('height'))
		self.MenuScrollPlay.add_widget(self.MenuScrollRoll)
		self.add_widget(self.MenuScrollPlay)
		# with self.MenuScrollPlay.canvas.before:
		# 	Color(1, 1, 1, 1)
		# 	self.rect = Rectangle(size=self.size, pos=self.pos)
		# self.MenuScrollPlay.bind(size=self._update_rect, pos=self._update_rect)
		self.MakeWhiteBack(self.MenuScrollPlay)
		self.ShowMenuContent()
		self.TransitionMenuOpen()

	def ShowMenuContent(self):
		self.MakeMenuTop()
		self.MenuScrollRoll.add_widget(self.MenuTop)
		self.MakeMenuGrid()
		self.MenuScrollRoll.add_widget(self.MenuGrid)
		for i in range(0):
			ThumbText = str(i+1)
			fun = partial(self.ChangeWindow,"Home")
			Thumb = Button(text=ThumbText,halign='center',font_size=25,size_hint_y=None,background_color=(1,0,0,0.9),font_name=FontDict["LobsterTwo-BoldItalic"],on_press=fun)
			Thumb.bind(width=lambda s,w: s.setter("text_size")(s,(w,None)))
			Thumb.bind(texture_size=Thumb.setter("size"))
			self.MenuScrollRoll.add_widget(Thumb)

	def MakeMenuTop(self):
		self.MenuTop = FloatLayout(size_hint=(1.0,None),height=150)

		self.MenuTopBack = ImageButton(source=AppImages["back"],allow_stretch=True,keep_ratio=False,size_hint=(1.0,None),height=150,pos_hint={"center_x":0.5,"center_y":0.5})
		self.MenuTop.add_widget(self.MenuTopBack)

		self.MenuTopDP = GridLayout(cols=1, spacing=1, size_hint=(0.19,0.59), pos_hint={"center_x":0.9,"center_y":0.6}, padding=1)
		ThumbPath = self.GetCurrUserInfo("dp")
		with self.MenuTopDP.canvas:
			self.MenuDP = Ellipse(source=ThumbPath,keep_ratio=True)
		self.MenuTopDP.bind(pos=partial(self.UpGridTop),size=partial(self.UpGridTop))
		self.MenuTop.add_widget(self.MenuTopDP)

		ThumbText = self.GetCurrUserInfo("name")
		self.MenuTopName = Button(text=ThumbText,halign='center', size_hint=(0.69,0.59), pos_hint={"center_x":0.35,"center_y":0.5},font_size=50,color=(0,0,0,0.9),background_color=(0.5,0.5,0.5,0.0),font_name=FontDict["LobsterTwo-BoldItalic"])
		self.MenuTop.add_widget(self.MenuTopName)

	def MakeMenuGrid(self):
		self.MenuGrid = GridLayout(cols=1,spacing=5,size_hint=(1.0,None),padding=10)
		self.MenuGrid.bind(minimum_height=self.MenuGrid.setter('height'))

		self.MenuTopics = {
			0:{"name":"Show Accounts","window":"ShowAccount"},
			1:{"name":"Show Expenses","window":"ShowExpense"},
			2:{"name":"Show Categories","window":"ShowCategory"}
		}

		for i in range(len(self.MenuTopics)):
			ThumbText = self.MenuTopics[i]["name"]
			fun = partial(self.ChangeWindow,self.MenuTopics[i]["window"])
			Thumb = Button(text=ThumbText,halign='center',font_size=35,size_hint_y=None,background_color=(0,102/255.0,204/255.0,0.99),font_name=FontDict["LobsterTwo-BoldItalic"],on_press=fun)
			Thumb.bind(width=lambda s,w: s.setter("text_size")(s,(w,None)))
			Thumb.bind(texture_size=Thumb.setter("size"))
			self.MenuGrid.add_widget(Thumb)

	def UpGridTop(self,*args):
		self.MenuDP.pos = self.MenuTopDP.pos
		self.MenuDP.size = self.MenuTopDP.size

	def TransitionMenuOpen(self,_="_"):
		anim_time = 0.25
		anim = Animation(pos_hint={"center_x":self.MenuScrollX,"center_y":self.MenuScrollY},duration=anim_time)
		anim.start(self.MenuScrollPlay)
		anim2 = Animation(clearcolor=(0.6,0.6,0.6,0.6),duration=anim_time)
		anim2.start(Window)
		self.MenuOpen = True

	def TransitionMenuClose(self,_="_"):
		anim_time = 0.25
		anim = Animation(pos_hint={"center_x":self.MenuHideScrollX,"center_y":self.MenuHideScrollY},duration=anim_time)
		anim.bind(on_start=lambda x,y: self.wait_anim(True),
            on_complete=lambda x,y: self.on_pre_enter())
		anim.start(self.MenuScrollPlay)
		anim2 = Animation(clearcolor=(1,1,1,1),duration=anim_time)
		anim2.start(Window)
		self.MenuOpen = False

	def wait_anim(self,x):
		self.anim_on = x
		self.anim_on = x

	############### Menu ###############

	############### category ###############
	def ShowCategories(self):
		self.MainScrollPlay = ScrollView(size_hint=(self.MainScrollW, self.MainScrollH),pos_hint={"center_x":self.MainScrollX,"center_y":self.MainScrollY}, size=(Window.width, Window.height))
		self.MainScrollRoll = GridLayout(cols=1, spacing=10, size_hint_y=None,padding=5)
		self.MainScrollRoll.bind(minimum_height=self.MainScrollRoll.setter('height'))
		self.MainScrollPlay.add_widget(self.MainScrollRoll)
		self.add_widget(self.MainScrollPlay)
		self.MakeWhiteBack(self.MainScrollPlay,partial(Color,0.9,0.9,0.9,0.8))
		self.AddCatMenu()

	def AddCatMenu(self):
		self.MainScrollRoll.clear_widgets()

		self.CatRoll = {}
		self.SubCatRoll = {}
		self.AddSubCatRoll = {}

		self.AddSubCatColor = {}
		self.AddSubCatText = {}
		self.AddSubCatBtn = {}

		self.NowCats = self.GetCurrUserInfo("categories")
		self.RefreshCatMenu()

	def RefreshCatMenu(self):
		self.MainScrollRoll.clear_widgets()
		for i in range(1,len(self.NowCats)+1):
			self.CatRoll[i] = GridLayout(cols=1,spacing=3,size_hint=(1.0,None),padding=2)
			self.CatRoll[i].bind(minimum_height=self.CatRoll[i].setter('height'))
			self.MainScrollRoll.add_widget(self.CatRoll[i])
			self.RefreshCat(i)

			Roll = GridLayout(cols=2,spacing=1,size_hint=(1.0,None),padding=1,height=80)
			Roll.bind(minimum_height=Roll.setter('height'))
			Thumb = Button(text="",size_hint_x=0.2,halign='center',font_size=25,size_hint_y=None,height=40,background_color=(0,0,0,0),background_normal="",font_name=FontDict["LobsterTwo-BoldItalic"])
			Thumb.bind(width=lambda s,w: s.setter("text_size")(s,(w,None)))
			Thumb.bind(texture_size=Thumb.setter("size"))
			Roll.add_widget(Thumb)
			self.SubCatRoll[i] = GridLayout(cols=1,spacing=3,size_hint=(0.8,None),padding=2)
			self.SubCatRoll[i].bind(minimum_height=self.SubCatRoll[i].setter('height'))
			Roll.add_widget(self.SubCatRoll[i])
			self.MainScrollRoll.add_widget(Roll)
			self.RefreshSubCat(i)

			Roll = GridLayout(cols=2,spacing=1,size_hint=(1.0,None),padding=1,height=80)
			Roll.bind(minimum_height=Roll.setter('height'))
			Thumb = Button(text="",size_hint_x=0.2,halign='center',font_size=25,size_hint_y=None,height=40,background_color=(0,0,0,0),background_normal="",font_name=FontDict["LobsterTwo-BoldItalic"])
			Thumb.bind(width=lambda s,w: s.setter("text_size")(s,(w,None)))
			Thumb.bind(texture_size=Thumb.setter("size"))
			Roll.add_widget(Thumb)
			self.AddSubCatRoll[i] = GridLayout(cols=1,spacing=3,size_hint=(0.8,None),padding=2)
			self.AddSubCatRoll[i].bind(minimum_height=self.AddSubCatRoll[i].setter('height'))
			Roll.add_widget(self.AddSubCatRoll[i])
			self.MainScrollRoll.add_widget(Roll)
			self.RefreshAddSubCat(i)

		self.AddCatRoll = GridLayout(cols=1,spacing=3,size_hint=(1.0,None),padding=2)
		self.AddCatRoll.bind(minimum_height=self.AddCatRoll.setter('height'))
		self.MainScrollRoll.add_widget(self.AddCatRoll)
		self.RefreshAddCat()

	def RefreshCat(self,i):
		self.CatRoll[i].clear_widgets()
		name = self.NowCats[str(i)]["name"]
		exp = self.NowCats[str(i)]["type"]
		name +=  " - " + exp*"Income" + (1-exp)*"Expense"
		Thumb = Button(text=name,halign='center',font_size=25,size_hint_y=None,height=50,background_color=self.NowCats[str(i)]["color"],background_normal="",font_name=FontDict["LobsterTwo-BoldItalic"])
		self.CatRoll[i].add_widget(Thumb)

	def RefreshSubCat(self,i):
		self.SubCatRoll[i].clear_widgets()
		for j in range(1,len(self.NowCats[str(i)]["sub_cats"])+1):
			name = self.NowCats[str(i)]["sub_cats"][str(j)]["name"]
			Thumb = Button(text=name,size_hint_x=0.8,halign='center',font_size=25,size_hint_y=None,height=40,background_color=self.NowCats[str(i)]["sub_cats"][str(j)]["color"],background_normal="",font_name=FontDict["LobsterTwo-BoldItalic"])
			self.SubCatRoll[i].add_widget(Thumb)

	def RefreshAddSubCat(self,i):
		self.AddSubCatRoll[i].clear_widgets()

		fun = partial(self.RefreshAddSubCatMain,i)
		name = self.NowCats[str(i)]["name"]
		exp = self.NowCats[str(i)]["type"]
		name +=  " - " + exp*"Income" + (1-exp)*"Expense"
		# self.AddSubCatColor[i] = self.all_colors[0]
		self.AddSubCatColor[i] = (0.5,0.5,0.5,0.5)
		self.AddSubCatBtn[i] = Button(text="Add Sub-Category In " + name,size_hint_x=0.2,valign="center",halign='center',font_size=25,size_hint_y=None,height=40,background_color=self.AddSubCatColor[i],background_normal="",font_name=FontDict["LobsterTwo-BoldItalic"],on_press=fun)
		self.AddSubCatRoll[i].add_widget(self.AddSubCatBtn[i])

	def RefreshAddSubCatMain(self,i,_="_"):
		self.AddSubCatRoll[i].clear_widgets()

		MainRoll = GridLayout(cols=2,spacing=1,size_hint=(1.0,None),padding=1,height=80)
		MainRoll.bind(minimum_height=MainRoll.setter('height'))
		self.AddSubCatRoll[i].add_widget(MainRoll)

		self.AddSubCatText[i] = TextInput(size_hint_x=0.4,valign="center",halign='center',font_size=25,size_hint_y=None,height=80,font_name=FontDict["LobsterTwo-BoldItalic"])
		MainRoll.add_widget(self.AddSubCatText[i])

		Roll = GridLayout(cols=4,spacing=3,size_hint=(1.0,None),padding=2,height=80)
		for j in range(len(self.all_colors)):
			fun = partial(self.ChangeNewColor,"sub",i,self.all_colors[j])
			Thumb = Button(text="",size_hint=(1.0,1.0),valign="center",halign='center',font_size=15,background_color=self.all_colors[j],background_normal="",font_name=FontDict["LobsterTwo-BoldItalic"],on_press=fun)
			Roll.add_widget(Thumb)
		MainRoll.add_widget(Roll)

		fun = partial(self.AddCat,"sub",i)
		name = self.NowCats[str(i)]["name"]
		exp = self.NowCats[str(i)]["type"]
		name +=  " - " + exp*"Income" + (1-exp)*"Expense"
		self.AddSubCatColor[i] = self.all_colors[0]
		self.AddSubCatBtn[i] = Button(text="Add Sub-Category In " + name,size_hint_x=0.2,valign="center",halign='center',font_size=25,size_hint_y=None,height=40,background_color=self.AddSubCatColor[i],background_normal="",font_name=FontDict["LobsterTwo-BoldItalic"],on_press=fun)
		self.AddSubCatRoll[i].add_widget(self.AddSubCatBtn[i])

	def RefreshAddCat(self):
		fun = partial(self.RefreshAddCatMain)
		self.AddCatRoll.clear_widgets()
		self.AddCatColor = (0.3,0.3,0.3,0.5)
		self.AddCatBtn = Button(text="Add Category",size_hint_x=0.2,valign="center",halign='center',font_size=25,size_hint_y=None,height=50,background_color=self.AddCatColor,background_normal="",font_name=FontDict["LobsterTwo-BoldItalic"],on_press=fun)
		self.AddCatRoll.add_widget(self.AddCatBtn)

	def RefreshAddCatMain(self,_="_"):
		self.AddCatRoll.clear_widgets()

		MainRoll = GridLayout(cols=2,spacing=1,size_hint=(1.0,None),padding=1,height=80)
		MainRoll.bind(minimum_height=MainRoll.setter('height'))
		self.AddCatRoll.add_widget(MainRoll)

		self.AddCatText = TextInput(size_hint_x=0.4,valign="center",halign='center',font_size=25,size_hint_y=None,height=80,font_name=FontDict["LobsterTwo-BoldItalic"])
		MainRoll.add_widget(self.AddCatText)

		Roll = GridLayout(cols=4,spacing=3,size_hint=(1.0,None),padding=2,height=80)
		for j in range(len(self.all_colors)):
			fun = partial(self.ChangeNewColor,"main",-1,self.all_colors[j])
			Thumb = Button(text="",size_hint=(1.0,1.0),valign="center",halign='center',font_size=15,background_color=self.all_colors[j],background_normal="",font_name=FontDict["LobsterTwo-BoldItalic"],on_press=fun)
			Roll.add_widget(Thumb)
		MainRoll.add_widget(Roll)

		fun = partial(self.AddCat,"main",0)
		self.AddCatColor = self.all_colors[1]
		self.AddCatBtnE = Button(text="Add Expense Category",size_hint_x=0.2,valign="center",halign='center',font_size=25,size_hint_y=None,height=50,background_color=self.AddCatColor,background_normal="",font_name=FontDict["LobsterTwo-BoldItalic"],on_press=fun)
		self.AddCatRoll.add_widget(self.AddCatBtnE)
		fun = partial(self.AddCat,"main",1)
		self.AddCatColor = self.all_colors[1]
		self.AddCatBtnI = Button(text="Add Income Category",size_hint_x=0.2,valign="center",halign='center',font_size=25,size_hint_y=None,height=50,background_color=self.AddCatColor,background_normal="",font_name=FontDict["LobsterTwo-BoldItalic"],on_press=fun)
		self.AddCatRoll.add_widget(self.AddCatBtnI)

	def ChangeNewColor(self,item_type,number,color,_="_"):
		if(item_type == "sub"):
			self.AddSubCatColor[number] = color
			self.AddSubCatBtn[number].background_color = color
		elif(item_type == "main"):
			self.AddCatColor = color
			self.AddCatBtnI.background_color = color
			self.AddCatBtnE.background_color = color

	def AddCat(self,item_type,number,_="_"):
		if(item_type == "sub"):
			MyDict = {"color":self.AddSubCatColor[number],"name":self.AddSubCatText[number].text}
			user = MainDict["now_user"]
			subs = MainDict["users"][user]["categories"][str(number)]["sub_cats"]
			MainDict["users"][user]["categories"][str(number)]["sub_cats"][str(len(subs)+1)] = MyDict
			SaveDict()
			self.RefreshSubCat(number)
			self.RefreshAddSubCat(number)
		if(item_type == "main"):
			MyDict = {"type":number,"color":self.AddCatColor,"name":self.AddCatText.text,"sub_cats":{"1":{"color":[1.0,0,0,1.0],"name":"default"}}}
			user = MainDict["now_user"]
			subs = MainDict["users"][user]["categories"]
			MainDict["users"][user]["categories"][str(len(subs)+1)] = MyDict
			SaveDict()
			self.RefreshCatMenu()

	############### category ###############

	############### account ###############
	def ShowAccounts(self):
		self.MainScrollPlay = ScrollView(size_hint=(self.MainScrollW, self.MainScrollH),pos_hint={"center_x":self.MainScrollX,"center_y":self.MainScrollY}, size=(Window.width, Window.height))
		self.MainScrollRoll = GridLayout(cols=1, spacing=10, size_hint_y=None,padding=5)
		self.MainScrollRoll.bind(minimum_height=self.MainScrollRoll.setter('height'))
		self.MainScrollPlay.add_widget(self.MainScrollRoll)
		self.add_widget(self.MainScrollPlay)
		self.MakeWhiteBack(self.MainScrollPlay,partial(Color,0.0,0.6,0.7,0.8))
		self.AddAccountMenu()

	def AddAccountMenu(self):
		self.MainScrollRoll.clear_widgets()

		self.AccNameRoll = {}
		self.AccBalRoll = {}
		self.AccDetRoll = {}
		self.AccAddDetRoll = {}

		self.NowAccs = self.GetCurrUserInfo("accounts")
		self.RefreshAccMenu()

	def RefreshAccMenu(self):
		print("adding accounts")
		self.MainScrollRoll.clear_widgets()
		for i in range(1,len(self.NowAccs)+1):
			self.AccNameRoll[i] = GridLayout(cols=1,spacing=3,size_hint=(1.0,None),padding=2)
			self.AccNameRoll[i].bind(minimum_height=self.AccNameRoll[i].setter('height'))
			self.MainScrollRoll.add_widget(self.AccNameRoll[i])
			self.RefreshAccName(i)

			Roll = GridLayout(cols=2,spacing=1,size_hint=(1.0,None),padding=1,height=80)
			Roll.bind(minimum_height=Roll.setter('height'))
			Thumb = Button(text="",size_hint_x=0.15,halign='center',font_size=25,size_hint_y=None,height=40,background_color=(0,0,0,0),background_normal="",font_name=FontDict["LobsterTwo-BoldItalic"])
			Thumb.bind(width=lambda s,w: s.setter("text_size")(s,(w,None)))
			Thumb.bind(texture_size=Thumb.setter("size"))
			Roll.add_widget(Thumb)
			self.AccBalRoll[i] = GridLayout(cols=1,spacing=3,size_hint=(0.85,None),padding=2)
			self.AccBalRoll[i].bind(minimum_height=self.AccBalRoll[i].setter('height'))
			Roll.add_widget(self.AccBalRoll[i])
			self.MainScrollRoll.add_widget(Roll)
			self.RefreshAccBal(i)

			Roll = GridLayout(cols=2,spacing=1,size_hint=(1.0,None),padding=1,height=80)
			Roll.bind(minimum_height=Roll.setter('height'))
			Thumb = Button(text="",size_hint_x=0.3,halign='center',font_size=25,size_hint_y=None,height=40,background_color=(0,0,0,0),background_normal="",font_name=FontDict["LobsterTwo-BoldItalic"])
			Thumb.bind(width=lambda s,w: s.setter("text_size")(s,(w,None)))
			Thumb.bind(texture_size=Thumb.setter("size"))
			Roll.add_widget(Thumb)
			self.AccDetRoll[i] = GridLayout(cols=1,spacing=3,size_hint=(0.7,None),padding=2)
			self.AccDetRoll[i].bind(minimum_height=self.AccDetRoll[i].setter('height'))
			Roll.add_widget(self.AccDetRoll[i])
			self.MainScrollRoll.add_widget(Roll)
			self.RefreshAccDet(i)

			Roll = GridLayout(cols=2,spacing=1,size_hint=(1.0,None),padding=1,height=80)
			Roll.bind(minimum_height=Roll.setter('height'))
			Thumb = Button(text="",size_hint_x=0.3,halign='center',font_size=25,size_hint_y=None,height=40,background_color=(0,0,0,0),background_normal="",font_name=FontDict["LobsterTwo-BoldItalic"])
			Thumb.bind(width=lambda s,w: s.setter("text_size")(s,(w,None)))
			Thumb.bind(texture_size=Thumb.setter("size"))
			Roll.add_widget(Thumb)
			self.AccAddDetRoll[i] = GridLayout(cols=1,spacing=3,size_hint=(0.7,None),padding=2)
			self.AccAddDetRoll[i].bind(minimum_height=self.AccAddDetRoll[i].setter('height'))
			Roll.add_widget(self.AccAddDetRoll[i])
			self.MainScrollRoll.add_widget(Roll)
			self.RefreshAccAddDet(i)

		self.AddAccRoll = GridLayout(cols=1,spacing=3,size_hint=(1.0,None),padding=2)
		self.AddAccRoll.bind(minimum_height=self.AddAccRoll.setter('height'))
		self.MainScrollRoll.add_widget(self.AddAccRoll)
		self.RefreshAddAcc()

	def RefreshAccName(self,i):
		self.AccNameRoll[i].clear_widgets()
		name = self.NowAccs[str(i)]["name"]
		color = self.NowAccs[str(i)]["color"]
		Thumb = Button(text=name,halign='center',font_size=25,size_hint_y=None,height=50,background_color=color,background_normal="",font_name=FontDict["LobsterTwo-BoldItalic"])
		self.AccNameRoll[i].add_widget(Thumb)

	def RefreshAccBal(self,i):
		self.AccBalRoll[i].clear_widgets()
		name = str(self.NowAccs[str(i)]["balance"])
		color = self.NowAccs[str(i)]["color"]
		Thumb = Button(text=name,halign='center',font_size=25,size_hint_y=None,height=50,background_color=color,background_normal="",font_name=FontDict["LobsterTwo-BoldItalic"])
		self.AccBalRoll[i].add_widget(Thumb)

	def RefreshAccDet(self,i):
		self.AccDetRoll[i].clear_widgets()
		dets = (self.NowAccs[str(i)]["details"])
		color = self.NowAccs[str(i)]["color"]
		# print(self.NowAccs)
		for j in range(1,len(dets)+1):
			name = self.NowAccs[str(i)]["details"][str(j)]["title"] + " - "
			name += self.NowAccs[str(i)]["details"][str(j)]["info"]
			Thumb = Button(text=name,halign='center',font_size=25,size_hint_y=None,height=50,background_color=color,background_normal="",font_name=FontDict["LobsterTwo-BoldItalic"])
			self.AccDetRoll[i].add_widget(Thumb)

	def RefreshAccAddDet(self,i):
		print(type(i),i,self.AccAddDetRoll)
		fun = partial(self.RefreshAccAddDetMain,i)
		self.AccAddDetRoll[i].clear_widgets()
		color = self.NowAccs[str(i)]["color"]
		self.AddCatBtn = Button(text="Add Details",size_hint_x=0.2,valign="center",halign='center',font_size=25,size_hint_y=None,height=50,background_color=color,background_normal="",font_name=FontDict["LobsterTwo-BoldItalic"],on_press=fun)
		self.AccAddDetRoll[i].add_widget(self.AddCatBtn)

	def RefreshAccAddDetMain(self,i,_="_"):
		self.AccAddDetRoll[i].clear_widgets()

		MainRoll = GridLayout(cols=2,spacing=1,size_hint=(1.0,None),padding=1,height=80)
		MainRoll.bind(minimum_height=MainRoll.setter('height'))
		self.AccAddDetRoll[i].add_widget(MainRoll)

		self.AccAddDetTitleText = TextInput(size_hint_x=0.5,valign="center",halign='center',font_size=25,size_hint_y=None,height=50,font_name=FontDict["LobsterTwo-BoldItalic"])
		MainRoll.add_widget(self.AccAddDetTitleText)

		self.AccAddDetInfoText = TextInput(size_hint_x=0.5,valign="center",halign='center',font_size=25,size_hint_y=None,height=50,font_name=FontDict["LobsterTwo-BoldItalic"])
		MainRoll.add_widget(self.AccAddDetInfoText)

		fun = partial(self.AddAccDet,i)
		color = self.NowAccs[str(i)]["color"]
		self.AddAccDetBtn = Button(text="Add Account Details",size_hint_x=0.2,valign="center",halign='center',font_size=25,size_hint_y=None,height=30,background_color=color,background_normal="",font_name=FontDict["LobsterTwo-BoldItalic"],on_press=fun)
		self.AccAddDetRoll[i].add_widget(self.AddAccDetBtn)

	def RefreshAddAcc(self):
		fun = partial(self.RefreshAddAccMain)
		self.AddAccRoll.clear_widgets()
		self.AddAccColor = (0.3,0.3,0.3,0.5)
		self.AddAccBtn = Button(text="Add Account",size_hint_x=0.2,valign="center",halign='center',font_size=25,size_hint_y=None,height=50,background_color=self.AddCatColor,background_normal="",font_name=FontDict["LobsterTwo-BoldItalic"],on_press=fun)
		self.AddAccRoll.add_widget(self.AddAccBtn)

	def AddAccDet(self,num,_="_"):
		MyDict = {}
		MyDict["title"] = self.AccAddDetTitleText.text
		MyDict["info"] = self.AccAddDetInfoText.text

		user = MainDict["now_user"]
		number = str(num)
		det_no = str(len(MainDict["users"][user]["accounts"][number]["details"])+1)
		MainDict["users"][user]["accounts"][number]["details"][det_no] = MyDict
		SaveDict()
		self.RefreshAccAddDet(num)
		self.RefreshAccDet(num)

	############### account ###############

	def MakeWhiteBack(self,Grid,color=-1):
		if color == -1:
			color = partial(Color,0.5,0.5,0.5,0.5)
		with Grid.canvas.before:
			# Color(color)
			color()
			self.rect = Rectangle(size=Grid.size, pos=Grid.pos)
		Grid.bind(size=self._update_rect, pos=self._update_rect)		

	def _update_rect(self, instance, value):
		self.rect.pos = instance.pos
		self.rect.size = instance.size

	def TransitionBtn(self,_="_"):
		anim = Animation(pos_hint={"center_x":self.TogBtnX,"center_y":self.TogBtnY})
		anim.start(self.TogBtn)

	def ChangeWindow(self,*args):
		Name = args[0]
		print(Name)
		if Name=="Menu":
			self.ShowMenu()
		elif self.MenuOpen:
			if(self.NowWindow != Name):
				self.LastWindow = self.NowWindow
				self.NowWindow = Name
				self.TransitionMenuClose()
				# self.on_pre_enter()
			else:
				self.TransitionMenuClose()
				self.NowWindow = Name
		else:
			self.LastWindow = self.NowWindow
			self.NowWindow = Name
			self.on_pre_enter()

	def GetCurrUserInfo(self,*args):
		cat = args[0]		
		if(cat=="dp"):
			dp = MainDict["users"][MainDict["now_user"]][cat]
			return dp
		if(cat=="name"):
			name = MainDict["users"][MainDict["now_user"]][cat]
			return name
		if(cat=="categories"):
			name = MainDict["users"][MainDict["now_user"]][cat]
			return name
		if(cat=="accounts"):
			name = MainDict["users"][MainDict["now_user"]][cat]
			return name

class MainClass(App):
	def build(self):
		ScreenMan = ScreenManagerbuild()
		ScreenMan.add_widget(HomeScreen(name='HomeWindow'))

		return ScreenMan

class ScreenManagerbuild(ScreenManager):
	pass
if __name__ == '__main__':
	LoadDict()
	MainClass().run()
