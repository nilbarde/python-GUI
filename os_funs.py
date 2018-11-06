from os import walk, listdir,stat
from os.path import getsize,isfile,getmtime,getctime
from time import ctime
from datetime import datetime
import subprocess

def get_folders(curr_folder="/media/",get_id=0):
	folders = []
	if(get_id==0):
		folders.append(curr_folder+'/')
		for (dirpath, dirnames, filenames) in walk(curr_folder):
			for fold in dirnames:
				folders.append(dirpath + '/' + fold + '/')
	elif(get_id==1):
		for (dirpath, dirnames, filenames) in walk(curr_folder):
			for fold in dirnames:
				folders.append(dirpath + '/' + fold + '/')
			break
	return folders

def get_files(root_folder,get_id=0):
	files = []
	if(get_id==0):
		folders = get_folders(root_folder,0)
	elif(get_id==1):
		folders = [root_folder+"/"]
	for folder in folders:
		files_fold = ([(folder+i) for i in listdir(folder) if isfile(folder+i)])
		files_fold.sort()
		files += files_fold
	return files

def get_size(file_path="."):
	size_ = (subprocess.check_output(['du','-sh', file_path.replace("//","/")]).split()[0])
	return str(size_)[2:-1]

def get_size_old(start_path = '.'):
	total_size = 0
	files = get_files(start_path,0)
	for file in files:
		total_size += getsize(file)
		# print(file,total_size)
	i=0
	while (total_size>1000.0):
		total_size /= 1000.0
		i += 1
	sizes = ["bytes","kb","mb","gb"]
	print(start_path)
	return (str(round(total_size,2))+" "+sizes[i])

def get_modified_time(file_path):
	ttt = getmtime(file_path)
	edited = str(datetime.fromtimestamp(int(ttt)))
	now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	if(edited[:-9]==now[:-9]):
		return(edited[-8:-3])
	else:
		return(edited[5:-9])

print(get_size("json_funs.py"))

