from os import walk,listdir
from os.path import dirname as os_dirname
from os.path import exists as os_exists
from os import makedirs as os_makedirs

def get_folders(curr_folder):
	folders = []
	for (dirpath, dirnames, filenames) in walk(curr_folder):
		for fold in dirnames:
			name = dirpath + '/' + fold + '/'
			name = name.replace("//","/")
			folders.append(name)
		# break
	return folders

def get_files(folder,exts=None,address=False):
	files_fold = ([(i) for i in listdir(folder) if ("." in i)])
	files_fold.sort()
	files_ext = []
	if not (exts is None):
		if(type("s")==type(exts)):
			exts = [exts]
		for filename in files_fold:
			for ext in exts:
				if(filename.endswith(ext)):
					files_ext.append(filename)
	if(exts is None):
		files_ext = files_fold
	files = []
	for filename in files_ext:
		name = ''
		if(address):
			name += folder + "/"
		name += filename
		name = name.replace("//","/")
		files.append(name)
	return files

def ensure_dir(file_path):
	if '/' in file_path:
		directory = os_dirname(file_path)
		if not os_exists(directory):
			os_makedirs(directory)
