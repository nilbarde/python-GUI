from tkinter import *
import tkinter.messagebox as tkm
import os
from os import walk
from PIL import ImageTk,Image
from tkinter import ttk

def ensure_dir(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

class build_world(Frame):

	def __init__(self, master = None):
		Frame.__init__(self, master)
		self.master=master

		self.init_window()

	def init_window(self):
		self.master.title('File Explorer')
		self.pack(fill=BOTH,expand=1)
		label = Label(self,text='hii')
		label.pack(padx=10,pady=10)
		self.folder_view(root_folder)		

	def define_geometry(self):
		screen_width = self.master.winfo_screenwidth()
		screen_height = self.master.winfo_screenheight()
		screen_resolution = '1280x720'
		print(screen_resolution)
		self.master.geometry(screen_resolution)

	def folder_view(self,fold_dir):
		curr_folder=fold_dir
		self.destroy_inwindow()
		self.master.title(fold_dir)
		menu = Menu(self.master)
		self.master.config(menu=menu)
		self.build_common_menu(menu,fold_dir)
		self.build_folder_menu(menu,fold_dir)

		folders,text_files,image_files,other_name = self.get_folder_contains(curr_folder)

		label_folder=ttk.Label(self,text="Folders - ")
		folder_buttons=dict()
		if len(folders):
			label_folder.grid(row=0,column=0)
		for folder_num in range (len(folders)):
			curr_fold=fold_dir
			folder_buttons[folder_num]=ttk.Button(self,width=25,text=folders[folder_num],command= lambda a=folder_num: self.folder_view(curr_fold+'/'+folders[a]))#lambda:action)
			x_co=int(folder_num/5)
			y_co=int((folder_num%5)+1)
			folder_buttons[folder_num].grid(row=x_co,column=y_co)
		x_co_b=int(((len(folders)-1)/5)+1)
		
		#creating text list
		label_texts=ttk.Label(self,text="Texts - ")
		text_buttons=dict()
		if len(text_files):
			label_texts.grid(row=x_co_b,column=0)
		for text_num in range (len(text_files)):
			curr_fold=fold_dir
			text_buttons[text_num]=ttk.Button(self,width=25,text=text_files[text_num],command= lambda a=text_num: self.open_file(curr_fold+'/'+text_files[a]))#lambda:action)
			x_co=int(text_num/5)
			y_co=int((text_num%5)+1)
			text_buttons[text_num].grid(row=x_co_b+x_co,column=y_co)
		x_co_b+=int(((len(text_files)-1)/5)+1)

		#creating image list
		label_images=ttk.Label(self,text="Images - ")
		image_buttons=dict()
		if len(image_files):
			label_images.grid(row=x_co_b,column=0)
		for image_num in range (len(image_files)):
			curr_fold=fold_dir
			image_buttons[image_num]=ttk.Button(self,width=25,text=image_files[image_num],command= lambda a=image_num: self.open_photo(curr_fold+'/'+image_files[a]))#lambda:action)
			x_co=int(image_num/5)
			y_co=int((image_num%5)+1)
			image_buttons[image_num].grid(row=x_co_b+2*x_co+1,column=y_co)
		
		can=dict()
		for image_num in range (len(image_files)):
			curr_fold=fold_dir
			my_img_o=Image.open(curr_fold+'/'+image_files[image_num])
			my_img=ImageTk.PhotoImage(my_img_o)
			if (my_img.width()>100):
				my_img_o=Image.open(curr_fold+'/'+image_files[image_num]).resize((100,int(my_img.height()*100/my_img.width())))
				my_img=ImageTk.PhotoImage(my_img_o)
			if (my_img.height()>100):
				my_img_o=Image.open(curr_fold+'/'+image_files[image_num]).resize((int(my_img.width()*100/my_img.height()),100))
				my_img=ImageTk.PhotoImage(my_img_o)
			can=Canvas(self,width=(my_img.width()),height=(my_img.height()) )
			x_co=int(image_num/5)
			y_co=int((image_num%5)+1)
			can.grid(row=x_co_b+2*x_co,column=y_co)
			can.my_img=my_img
			can.create_image(0,0,anchor=NW,image=my_img)
			self.update_idletasks()
			self.update()

		x_co_b+=int((2*(len(image_files))-1/5)+1)

		#creating other file list
		label_other=ttk.Label(self,text="Others - ")
		other_buttons=dict()
		if len(other_name):
			label_other.grid(row=x_co_b,column=0)
		for other_num in range (len(other_name)):
			curr_fold=fold_dir
			other_buttons[other_num]=ttk.Button(self,width=25,text=other_name[other_num],command= lambda a=other_num: self.open_file(curr_fold+'/'+other_files[a]))#lambda:action)
			x_co=int(other_num/5)
			y_co=int((other_num%5)+1)
			other_buttons[other_num].grid(row=x_co_b+x_co,column=y_co)
		x_co_b+=int(((len(other_name)-1)/5)+1)

		#creating back button
		just_int=0
		for i_in_dir_length in range(len(curr_folder)-2):
			if (curr_folder[i_in_dir_length] == "/"):
				just_int=i_in_dir_length
		back_dir=curr_folder[:just_int+1]
		back_button=ttk.Button(self,text="Go Back",command= lambda:self.folder_view(back_dir),width=50)
		back_button.grid(row=int(x_co_b),column=2,columnspan=3)
		self.define_geometry()
		self.update_idletasks()
		self.update()

	def save_text_folder(self,fold_dir,text):
		curr_folder=fold_dir
		self.destroy_inwindow()
		self.master.title(fold_dir)
		menu = Menu(self.master)
		self.master.config(menu=menu)

		folders,text_files,image_files,other_name = self.get_folder_contains(curr_folder)

		label_folder=ttk.Label(self,text="Folders - ")
		folder_buttons=dict()
		if len(folders):
			label_folder.grid(row=0,column=0)
		for folder_num in range (len(folders)):
			curr_fold=fold_dir
			folder_buttons[folder_num]=ttk.Button(self,width=25,text=folders[folder_num],command= lambda a=folder_num: self.save_text_folder(curr_fold+'/'+folders[a],text))#lambda:action)
			x_co=int(folder_num/5)
			y_co=int((folder_num%5)+1)
			folder_buttons[folder_num].grid(row=x_co,column=y_co)
		x_co_b=int(((len(folders)-1)/5)+1)
		
		#creating text list
		label_texts=ttk.Label(self,text="Texts - ")
		text_buttons=dict()
		if len(text_files):
			label_texts.grid(row=x_co_b,column=0)
		for text_num in range (len(text_files)):
			curr_fold=fold_dir
			text_buttons[text_num]=ttk.Button(self,width=25,text=text_files[text_num])#lambda:action)
			x_co=int(text_num/5)
			y_co=int((text_num%5)+1)
			text_buttons[text_num].grid(row=x_co_b+x_co,column=y_co)
		x_co_b+=int(((len(text_files)-1)/5)+1)

		just_int=0
		for i_in_dir_length in range(len(curr_folder)-2):
			if (curr_folder[i_in_dir_length] == "/"):
				just_int=i_in_dir_length
		back_dir=curr_folder[:just_int+1]
		back_button=ttk.Button(self,text="Go Back",command= lambda:self.save_text_folder(back_dir,text),width=50)
		back_button.grid(row=int(int((len(folders)-1)/5+1)+int((len(text_files)-1)/5)+1),column=2,columnspan=3)
		name_button=ttk.Button(self,text="Save File",command= lambda :[self.save_file(fold_dir,text)],width=70)
		name_button.grid(row=int(int((len(folders)-1)/5+2)+int((len(text_files)-1)/5)+1),column=2,columnspan=3)	
	
	def save_file(self,fold_dir,text_save):
		name='name.txt'
		pop = Tk()
		text_window = Text(pop, height=20, width=60)
		text_window.insert(END, "write file name here")
		text_window.pack()

		btn_yes = ttk.Button(pop, text='OK',command = lambda :[self.write_text_file(fold_dir +'/'+ str(text_window.get("1.0","end-1c")),text_save) , pop.destroy()])
		btn_yes.pack()
		pop.mainloop()

	def write_text_file(self,fold_dir,text_save):
		file = open(fold_dir,'w')
		file.write(str(text_save))
		file.close()
		self.open_file(fold_dir)

	def new_file(self,now_fold):
		self.destroy_inwindow()
		menu = Menu(self.master)
		self.master.config(menu=menu)
		self.build_common_menu(menu,now_fold)
		submenu_text = Menu(menu)
		menu.add_cascade(label="edit" , menu=submenu_text)
		submenu_text.add_command(label="Save As File" , command=lambda:self.save_text_folder(now_fold,text=text_window.get("1.0","end-1c")))

		text_window = Text(self, height=60, width=100)
		text_window.insert(END, "write story here")
		text_window.pack()

	def open_file(self,file_name):
		self.destroy_inwindow()
		self.master.title(file_name)
		menu = Menu(self.master)
		self.master.config(menu=menu)
		self.build_common_menu(menu,file_name)
		submenu_text = Menu(menu)

		menu.add_cascade(label="edit" , menu=submenu_text)
		submenu_text.add_command(label="Save As File" , command=lambda:self.save_text_folder(file_name,text=text_window.get("1.0","end-1c")))
		submenu_text.add_command(label="Save File" , command=lambda:self.write_text_file(file_name,text_save=text_window.get("1.0","end-1c")))
		
		text_window = Text(self, height=100, width=200)
		text_window.pack()
		file_read=open(file_name,"r")
		story=file_read.read()
		text_window.insert(END, story)

	def build_common_menu(self,menu,now_fold):		
		submenu_gen = Menu(menu)
		menu.add_cascade(label="File" , menu=submenu_gen)

		submenu_gen.add_command(label="New File" , command=lambda:self.new_file(now_fold))
		submenu_gen.add_command(label="Open Root" , command=lambda:self.folder_view(root_folder))
		submenu_gen.add_command(label="Open Home" , command=lambda:self.folder_view(home_folder))
		submenu_gen.add_separator()

	def build_folder_menu(self,menu,now_fold):
		submenu_fold = Menu(menu)
		menu.add_cascade(label="edit" , menu=submenu_fold)
		submenu_fold.add_command(label="Rename Files" , command=lambda:self.files_rename(now_fold))
		#submenu_fold.add_command(label="Open Root" , command=lambda:folder_view(root_folder))
		
	def files_rename(self,now_fold):
		global can_call
		can_call= False
		pop = Tk()
		pop.title('WARNING')
		warn_label = ttk.Label(pop,text='Do You really want to rename all files in this directory ?')
		btn_yes = ttk.Button(pop, text='YES',command = lambda :[pop.destroy() , self.rename_files(now_fold)])
		btn_no = ttk.Button(pop, text='NO',command = lambda :[pop.destroy()])

		warn_label.grid(row=0,column=0,columnspan=3)
		btn_yes.grid(row=2,column=0)
		btn_no.grid(row=2,column=2)
		pop.mainloop()
		
	def rename_files(self,now_fold):
		pop2 = Tk()
		text_window = Text(pop2, height=20, width=60)
		text_window.insert(END, "write file extension here")
		text_window.pack()

		btn_yes = ttk.Button(pop2, text='OK',command = lambda :[self.rename_actual(now_fold,ext = text_window.get("1.0","end-1c")) , pop2.destroy()])
		btn_yes.pack()
		pop2.mainloop()
		
	def rename_actual(self,curr_folder,ext):
		for (dirpath, dirnames, filenames) in walk(curr_folder):
			i=1
			for name in filenames:
				if (name.endswith(ext)):
					ori_dir=(dirpath+'/'+name)
					destination=(dirpath+'/a'+'/'+str(i)+'.'+ext)
					i+=1
					ensure_dir(destination)	
					print(ori_dir)			
					os.rename(ori_dir, destination)

			for (dirpath2, dirnames, filenames) in walk(dirpath+'/a'):
				for name in filenames:
					if (name.endswith(ext)):
						ori_dir=(dirpath2+'/'+name)
						destination=(dirpath+'/'+name)
						ensure_dir(destination)
						os.rename(ori_dir, destination)
				os.rmdir(dirpath2)
		self.folder_view(curr_folder)

	def get_folder_contains(self,fold):
		folders=[]
		text_name=[]
		image_name=[]
		other_name=[]
		for (dirpath, dirnames, filenames) in os.walk(fold):
			for name in dirnames:
				folders.append(name)
			for names in filenames:
				if (int(names.endswith('.txt'))+int(names.endswith('.py'))+int(names.endswith('.cpp'))):
					text_name.append(names)
				elif (int(names.endswith('.jpg'))+int(names.endswith('.JPG'))+int(names.endswith('.jpeg'))+int(names.endswith('.JPEG'))+int(names.endswith('.png'))+int(names.endswith('.PNG'))+int(names.endswith('.gif'))):
					image_name.append(names)
				else:
					other_name.append(names)
			break
		return folders,text_name,image_name,other_name


	def change_can_call(self):
		global can_call
		can_call=True

	def destroy_inwindow(self):
		for widget in self.winfo_children():
			widget.destroy()


can_call=False

root_folder = os.path.dirname(os.path.realpath(__file__))
home_folder = '/media/nil/NIHAL/Nil'

root = Tk()

root.geometry('1280x720')

app = build_world (root)

root.mainloop()








