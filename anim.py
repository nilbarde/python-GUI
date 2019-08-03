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
		CatCodes = [i for i in self.NowCats]
		CatCodes.sort()
		for CatCode in CatCodes:
			self.CatRoll[CatCode] = GridLayout(cols=1,spacing=3,size_hint=(1.0,None),padding=2)
			self.CatRoll[CatCode].bind(minimum_height=self.CatRoll[CatCode].setter('height'))
			self.MainScrollRoll.add_widget(self.CatRoll[CatCode])
			self.RefreshCat(CatCode)

			Roll = GridLayout(cols=2,spacing=1,size_hint=(1.0,None),padding=1,height=80)
			Roll.bind(minimum_height=Roll.setter('height'))
			Thumb = Button(text="",size_hint_x=0.2,halign='center',font_size=25,size_hint_y=None,height=40,background_color=(0,0,0,0),background_normal="",font_name=FontDict["LobsterTwo-BoldItalic"])
			Thumb.bind(width=lambda s,w: s.setter("text_size")(s,(w,None)))
			Thumb.bind(texture_size=Thumb.setter("size"))
			Roll.add_widget(Thumb)
			self.SubCatRoll[CatCode] = GridLayout(cols=1,spacing=3,size_hint=(0.8,None),padding=2)
			self.SubCatRoll[CatCode].bind(minimum_height=self.SubCatRoll[CatCode].setter('height'))
			Roll.add_widget(self.SubCatRoll[CatCode])
			self.MainScrollRoll.add_widget(Roll)
			self.RefreshSubCat(CatCode)

			Roll = GridLayout(cols=2,spacing=1,size_hint=(1.0,None),padding=1,height=80)
			Roll.bind(minimum_height=Roll.setter('height'))
			Thumb = Button(text="",size_hint_x=0.2,halign='center',font_size=25,size_hint_y=None,height=40,background_color=(0,0,0,0),background_normal="",font_name=FontDict["LobsterTwo-BoldItalic"])
			Thumb.bind(width=lambda s,w: s.setter("text_size")(s,(w,None)))
			Thumb.bind(texture_size=Thumb.setter("size"))
			Roll.add_widget(Thumb)
			self.AddSubCatRoll[CatCode] = GridLayout(cols=1,spacing=3,size_hint=(0.8,None),padding=2)
			self.AddSubCatRoll[CatCode].bind(minimum_height=self.AddSubCatRoll[CatCode].setter('height'))
			Roll.add_widget(self.AddSubCatRoll[CatCode])
			self.MainScrollRoll.add_widget(Roll)
			self.RefreshAddSubCat(CatCode)

		self.AddCatRoll = GridLayout(cols=1,spacing=3,size_hint=(1.0,None),padding=2)
		self.AddCatRoll.bind(minimum_height=self.AddCatRoll.setter('height'))
		self.MainScrollRoll.add_widget(self.AddCatRoll)
		self.RefreshAddCat()

	def RefreshCat(self,CatCode):
		self.CatRoll[CatCode].clear_widgets()
		name = self.NowCats[CatCode]["name"]
		exp = self.NowCats[CatCode]["type"]
		name +=  " - " + exp*"Income" + (1-exp)*"Expense"
		color = self.NowCats[CatCode]["color"]
		Thumb = Button(text=name,halign='center',font_size=25,size_hint_y=None,height=50,background_color=color,background_normal="",font_name=FontDict["LobsterTwo-BoldItalic"])
		self.CatRoll[CatCode].add_widget(Thumb)

	def RefreshSubCat(self,CatCode):
		self.SubCatRoll[CatCode].clear_widgets()
		SubCatCodes = [i for i in self.NowCats[CatCode]["sub_cats"]]
		SubCatCodes.sort()
		# for j in range(1,len(self.NowCats[str(i)]["sub_cats"])+1):
		for SubCatCode in SubCatCodes:
			name = self.NowCats[CatCode]["sub_cats"][SubCatCode]["name"]
			color = self.NowCats[CatCode]["sub_cats"][SubCatCode]["color"]
			Thumb = Button(text=name,size_hint_x=0.8,halign='center',font_size=25,size_hint_y=None,height=40,background_color=color,background_normal="",font_name=FontDict["LobsterTwo-BoldItalic"])
			self.SubCatRoll[CatCode].add_widget(Thumb)

	def RefreshAddSubCat(self,CatCode):
		self.AddSubCatRoll[CatCode].clear_widgets()

		fun = partial(self.RefreshAddSubCatMain,CatCode)
		name = self.NowCats[CatCode]["name"]
		exp = self.NowCats[CatCode]["type"]
		name +=  " - " + exp*"Income" + (1-exp)*"Expense"
		# self.AddSubCatColor[i] = self.all_colors[0]
		self.AddSubCatColor[CatCode] = (0.5,0.5,0.5,0.5)
		color = self.AddSubCatColor[CatCode]
		self.AddSubCatBtn[CatCode] = Button(text="Add Sub-Category In " + name,size_hint_x=0.2,valign="center",halign='center',font_size=25,size_hint_y=None,height=40,background_color=color,background_normal="",font_name=FontDict["LobsterTwo-BoldItalic"],on_press=fun)
		self.AddSubCatRoll[CatCode].add_widget(self.AddSubCatBtn[CatCode])

	def RefreshAddSubCatMain(self,CatCode,_="_"):
		self.AddSubCatRoll[CatCode].clear_widgets()

		MainRoll = GridLayout(cols=2,spacing=1,size_hint=(1.0,None),padding=1,height=80)
		MainRoll.bind(minimum_height=MainRoll.setter('height'))
		self.AddSubCatRoll[CatCode].add_widget(MainRoll)

		self.AddSubCatText[CatCode] = TextInput(size_hint_x=0.4,valign="center",halign='center',font_size=25,size_hint_y=None,height=80,font_name=FontDict["LobsterTwo-BoldItalic"])
		MainRoll.add_widget(self.AddSubCatText[CatCode])

		Roll = GridLayout(cols=4,spacing=3,size_hint=(1.0,None),padding=2,height=80)
		for j in range(len(self.all_colors)):
			fun = partial(self.ChangeNewColor,"sub",CatCode,self.all_colors[j])
			Thumb = Button(text="",size_hint=(1.0,1.0),valign="center",halign='center',font_size=15,background_color=self.all_colors[j],background_normal="",font_name=FontDict["LobsterTwo-BoldItalic"],on_press=fun)
			Roll.add_widget(Thumb)
		MainRoll.add_widget(Roll)

		fun = partial(self.AddCat,"sub",CatCode)
		name = self.NowCats[CatCode]["name"]
		exp = self.NowCats[CatCode]["type"]
		name +=  " - " + exp*"Income" + (1-exp)*"Expense"
		self.AddSubCatColor[CatCode] = self.all_colors[0]
		color = self.AddSubCatColor[CatCode]
		self.AddSubCatBtn[CatCode] = Button(text="Add Sub-Category In " + name,size_hint_x=0.2,valign="center",halign='center',font_size=25,size_hint_y=None,height=40,background_color=color,background_normal="",font_name=FontDict["LobsterTwo-BoldItalic"],on_press=fun)
		self.AddSubCatRoll[CatCode].add_widget(self.AddSubCatBtn[CatCode])

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

	def ChangeNewColor(self,item_type,CatCode,color,_="_"):
		if(item_type == "sub"):
			self.AddSubCatColor[CatCode] = color
			self.AddSubCatBtn[CatCode].background_color = color
		elif(item_type == "main"):
			self.AddCatColor = color
			self.AddCatBtnI.background_color = color
			self.AddCatBtnE.background_color = color

	def AddCat(self,item_type,CatCode,_="_"):
		if(item_type == "sub"):
			MyDict = {"color":self.AddSubCatColor[CatCode],"name":self.AddSubCatText[CatCode].text}
			user = MainDict["now_user"]
			MainDict["users"][user]["categories"][CatCode]["sub_count"] += 1
			new_code = self.get_code(MainDict["users"][user]["categories"][CatCode]["sub_count"],4)
			# subs = MainDict["users"][user]["categories"][str(CatCode)]["sub_cats"]
			MainDict["users"][user]["categories"][CatCode]["sub_cats"][new_code] = MyDict
			SaveDict()
			self.RefreshSubCat(CatCode)
			self.RefreshAddSubCat(CatCode)
		if(item_type == "main"):
			MyDict = {"type":CatCode,"color":self.AddCatColor,"name":self.AddCatText.text,"sub_cats":{"1":{"color":[1.0,0,0,1.0],"name":"default"}}}
			user = MainDict["now_user"]
			# subs = MainDict["users"][user]["categories"]
			MainDict["users"][user]["count"]["categories"] += 1
			new_code = self.get_code(MainDict["users"][user]["count"]["categories"],4)
			MainDict["users"][user]["categories"][new_code] = MyDict
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
		self.MainScrollRoll.clear_widgets()
		AccCodes = [i for i in self.NowAccs]
		AccCodes.sort()
		for AccCode in AccCodes:
			self.AccNameRoll[AccCode] = GridLayout(cols=1,spacing=3,size_hint=(1.0,None),padding=2)
			self.AccNameRoll[AccCode].bind(minimum_height=self.AccNameRoll[AccCode].setter('height'))
			self.MainScrollRoll.add_widget(self.AccNameRoll[AccCode])
			self.RefreshAccName(AccCode)

			Roll = GridLayout(cols=2,spacing=1,size_hint=(1.0,None),padding=1,height=80)
			Roll.bind(minimum_height=Roll.setter('height'))
			Thumb = Button(text="",size_hint_x=0.15,halign='center',font_size=25,size_hint_y=None,height=40,background_color=(0,0,0,0),background_normal="",font_name=FontDict["LobsterTwo-BoldItalic"])
			Thumb.bind(width=lambda s,w: s.setter("text_size")(s,(w,None)))
			Thumb.bind(texture_size=Thumb.setter("size"))
			Roll.add_widget(Thumb)
			self.AccBalRoll[AccCode] = GridLayout(cols=1,spacing=3,size_hint=(0.85,None),padding=2)
			self.AccBalRoll[AccCode].bind(minimum_height=self.AccBalRoll[AccCode].setter('height'))
			Roll.add_widget(self.AccBalRoll[AccCode])
			self.MainScrollRoll.add_widget(Roll)
			self.RefreshAccBal(AccCode)

			Roll = GridLayout(cols=2,spacing=1,size_hint=(1.0,None),padding=1,height=80)
			Roll.bind(minimum_height=Roll.setter('height'))
			Thumb = Button(text="",size_hint_x=0.3,halign='center',font_size=25,size_hint_y=None,height=40,background_color=(0,0,0,0),background_normal="",font_name=FontDict["LobsterTwo-BoldItalic"])
			Thumb.bind(width=lambda s,w: s.setter("text_size")(s,(w,None)))
			Thumb.bind(texture_size=Thumb.setter("size"))
			Roll.add_widget(Thumb)
			self.AccDetRoll[AccCode] = GridLayout(cols=1,spacing=3,size_hint=(0.7,None),padding=2)
			self.AccDetRoll[AccCode].bind(minimum_height=self.AccDetRoll[AccCode].setter('height'))
			Roll.add_widget(self.AccDetRoll[AccCode])
			self.MainScrollRoll.add_widget(Roll)
			self.RefreshAccDet(AccCode)

			Roll = GridLayout(cols=2,spacing=1,size_hint=(1.0,None),padding=1,height=80)
			Roll.bind(minimum_height=Roll.setter('height'))
			Thumb = Button(text="",size_hint_x=0.3,halign='center',font_size=25,size_hint_y=None,height=40,background_color=(0,0,0,0),background_normal="",font_name=FontDict["LobsterTwo-BoldItalic"])
			Thumb.bind(width=lambda s,w: s.setter("text_size")(s,(w,None)))
			Thumb.bind(texture_size=Thumb.setter("size"))
			Roll.add_widget(Thumb)
			self.AccAddDetRoll[AccCode] = GridLayout(cols=1,spacing=3,size_hint=(0.7,None),padding=2)
			self.AccAddDetRoll[AccCode].bind(minimum_height=self.AccAddDetRoll[AccCode].setter('height'))
			Roll.add_widget(self.AccAddDetRoll[AccCode])
			self.MainScrollRoll.add_widget(Roll)
			self.RefreshAccAddDet(AccCode)

		self.AddAccRoll = GridLayout(cols=1,spacing=3,size_hint=(1.0,None),padding=2)
		self.AddAccRoll.bind(minimum_height=self.AddAccRoll.setter('height'))
		self.MainScrollRoll.add_widget(self.AddAccRoll)
		self.RefreshAddAcc()

	def RefreshAccName(self,AccCode):
		self.AccNameRoll[AccCode].clear_widgets()
		name = self.NowAccs[AccCode]["name"]
		color = self.NowAccs[AccCode]["color"]
		Thumb = Button(text=name,halign='center',font_size=25,size_hint_y=None,height=50,background_color=color,background_normal="",font_name=FontDict["LobsterTwo-BoldItalic"])
		self.AccNameRoll[AccCode].add_widget(Thumb)

	def RefreshAccBal(self,AccCode):
		self.AccBalRoll[AccCode].clear_widgets()
		name = "Rs. " + str(self.NowAccs[AccCode]["balance"])
		color = self.NowAccs[AccCode]["color"]
		Thumb = Button(text=name,halign='center',font_size=25,size_hint_y=None,height=50,background_color=color,background_normal="",font_name=FontDict["LobsterTwo-BoldItalic"])
		self.AccBalRoll[AccCode].add_widget(Thumb)

	def RefreshAccDet(self,AccCode):
		self.AccDetRoll[AccCode].clear_widgets()
		dets = (self.NowAccs[AccCode]["details"])
		color = self.NowAccs[AccCode]["color"]
		# print(self.NowAccs)
		DetCodes = [i for i in dets]
		DetCodes.sort()
		# for j in range(1,len(dets)+1):
		for DetCode in DetCodes:
			name = self.NowAccs[AccCode]["details"][DetCode]["title"] + " - "
			name += self.NowAccs[AccCode]["details"][DetCode]["info"]
			Thumb = Button(text=name,halign='center',font_size=25,size_hint_y=None,background_color=color,background_normal="",font_name=FontDict["LobsterTwo-BoldItalic"])
			Thumb.bind(width=lambda s,w: s.setter("text_size")(s,(w,None)))
			Thumb.bind(texture_size=Thumb.setter("size"))
			self.AccDetRoll[AccCode].add_widget(Thumb)
		if not len(dets):
			print("shrink")
			color[-1] *= 0.5
			Thumb = Button(text="No Details Available",halign='center',font_size=25,size_hint_y=None,background_color=color,background_normal="",font_name=FontDict["LobsterTwo-BoldItalic"])
			Thumb.bind(width=lambda s,w: s.setter("text_size")(s,(w,None)))
			Thumb.bind(texture_size=Thumb.setter("size"))
			self.AccDetRoll[AccCode].add_widget(Thumb)

	def RefreshAccAddDet(self,AccCode):
		fun = partial(self.RefreshAccAddDetMain,AccCode)
		self.AccAddDetRoll[AccCode].clear_widgets()
		color = self.NowAccs[AccCode]["color"]
		self.AddCatBtn = Button(text="Add Details",size_hint_x=0.2,valign="center",halign='center',font_size=25,size_hint_y=None,height=50,background_color=color,background_normal="",font_name=FontDict["LobsterTwo-BoldItalic"],on_press=fun)
		self.AccAddDetRoll[AccCode].add_widget(self.AddCatBtn)

	def RefreshAccAddDetMain(self,AccCode,_="_"):
		self.AccAddDetRoll[AccCode].clear_widgets()

		MainRoll = GridLayout(cols=2,spacing=1,size_hint=(1.0,None),padding=1,height=80)
		MainRoll.bind(minimum_height=MainRoll.setter('height'))
		self.AccAddDetRoll[AccCode].add_widget(MainRoll)

		self.AccAddDetTitleText = TextInput(size_hint_x=0.5,valign="center",halign='center',font_size=25,size_hint_y=None,height=50,font_name=FontDict["LobsterTwo-BoldItalic"])
		MainRoll.add_widget(self.AccAddDetTitleText)

		self.AccAddDetInfoText = TextInput(size_hint_x=0.5,valign="center",halign='center',font_size=25,size_hint_y=None,height=50,font_name=FontDict["LobsterTwo-BoldItalic"])
		MainRoll.add_widget(self.AccAddDetInfoText)

		fun = partial(self.AddAccDet,AccCode)
		color = self.NowAccs[AccCode]["color"]
		self.AddAccDetBtn = Button(text="Add Account Details",size_hint_x=0.2,valign="center",halign='center',font_size=25,size_hint_y=None,height=30,background_color=color,background_normal="",font_name=FontDict["LobsterTwo-BoldItalic"],on_press=fun)
		self.AccAddDetRoll[AccCode].add_widget(self.AddAccDetBtn)

	def RefreshAddAcc(self):
		fun = partial(self.RefreshAddAccMain)
		self.AddAccRoll.clear_widgets()
		self.AddAccColor = (0.3,0.3,0.3,0.5)
		self.AddAccBtn = Button(text="Add Account",size_hint_x=0.2,valign="center",halign='center',font_size=25,size_hint_y=None,height=50,background_color=self.AddAccColor,background_normal="",font_name=FontDict["LobsterTwo-BoldItalic"],on_press=fun)
		self.AddAccRoll.add_widget(self.AddAccBtn)

	def RefreshAddAccMain(self,_="_"):
		self.AddAccRoll.clear_widgets()
		self.AddAccColor = self.all_colors[4]

		MainRoll = GridLayout(cols=2,spacing=1,size_hint=(1.0,None),padding=1,height=120)
		# MainRoll.bind(minimum_height=MainRoll.setter('height'))
		self.AddAccRoll.add_widget(MainRoll)

		SubRoll = GridLayout(cols=2,spacing=1,size_hint=(1.0,None),padding=1)
		MainRoll.add_widget(SubRoll)

		btn = Button(text="Name : ",size_hint=(0.4,1.0),valign="center",halign='center',font_size=25,background_color=(0.0,0.6,0.7,0.8),background_normal="",font_name=FontDict["LobsterTwo-BoldItalic"])
		SubRoll.add_widget(btn)

		self.AddAccName = TextInput(size_hint=(0.6,1.0),valign="center",halign='center',font_size=25,font_name=FontDict["LobsterTwo-BoldItalic"],foreground_color=self.AddAccColor)
		SubRoll.add_widget(self.AddAccName)

		btn = Button(text="Balance : ",size_hint=(0.4,1.0),valign="center",halign='center',font_size=25,background_color=(0.0,0.6,0.7,0.8),background_normal="",font_name=FontDict["LobsterTwo-BoldItalic"])
		SubRoll.add_widget(btn)

		self.AddAccBal = TextInput(size_hint=(0.6,1.0),valign="center",halign='center',font_size=25,font_name=FontDict["LobsterTwo-BoldItalic"],foreground_color=self.AddAccColor)
		SubRoll.add_widget(self.AddAccBal)

		Roll = GridLayout(cols=4,spacing=3,size_hint=(1.0,None),padding=2)
		for j in range(len(self.all_colors)):
			fun = partial(self.NewAccColor,self.all_colors[j])
			Thumb = Button(text="",size_hint=(1.0,1.0),valign="center",halign='center',font_size=15,background_color=self.all_colors[j],background_normal="",font_name=FontDict["LobsterTwo-BoldItalic"],on_press=fun)
			Roll.add_widget(Thumb)
		MainRoll.add_widget(Roll)

		fun = partial(self.AddAcc)
		self.AddAccBtn = Button(text="Add Account",size_hint_x=1.0,valign="center",halign='center',font_size=25,size_hint_y=None,height=50,background_color=self.AddAccColor,background_normal="",font_name=FontDict["LobsterTwo-BoldItalic"],on_press=fun)
		self.AddAccRoll.add_widget(self.AddAccBtn)

	def NewAccColor(self,color,_="_"):
		self.AddAccColor = color
		self.AddAccName.foreground_color = color
		self.AddAccBal.foreground_color = color
		self.AddAccBtn.background_color = color

	def AddAccDet(self,AccCode,_="_"):
		MyDict = {}
		MyDict["title"] = self.AccAddDetTitleText.text
		MyDict["info"] = self.AccAddDetInfoText.text

		user = MainDict["now_user"]
		MainDict["users"][user]["accounts"][AccCode]["details_count"] += 1
		new_code = self.get_code(MainDict["users"][user]["accounts"][AccCode]["details_count"],4)
		MainDict["users"][user]["accounts"][AccCode]["details"][new_code] = MyDict
		SaveDict()
		self.RefreshAccAddDet(AccCode)
		self.RefreshAccDet(AccCode)

	def AddAcc(self,_="_"):
		MyDict = {"color":self.AddAccColor,"name":self.AddAccName.text,"balance":float(self.AddAccBal.text),"details":{}}
		user = MainDict["now_user"]
		MainDict["users"][user]["count"]["accounts"] += 1
		new_code = self.get_code(MainDict["users"][user]["count"]["accounts"],4)
		MainDict["users"][user]["accounts"][new_code] = MyDict
		SaveDict()
		self.RefreshAccMenu()

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

	def get_code(self,num,bit):
		code = str(num)
		code = (bit-len(code))*"0" + code
		return code

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
