from json import dump as j_dump
from json import load as j_load
from codecs import open as co_open
from os import makedirs
from os.path import exists,dirname,isfile

def write_json(dict_,file_path):
	# print(file_path)
	ensure_dir(file_path)
	j_dump(dict_, co_open(file_path, 'w', encoding='utf-8'), separators=(',', ':'), sort_keys=True, indent=4)

def json_loader(filepath):
	# print(filepath)
	file = open(filepath)
	print(filepath)
	dict_ = j_load(file)
	return dict_

def ensure_dir(file_path):
	if("/" in file_path):
		directory = dirname(file_path)
		if not exists(directory):
			makedirs(directory)

