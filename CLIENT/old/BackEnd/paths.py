#IMPORT GENERAL
from os.path import join
"""
Images relative to execute.py
"""

#IMPORT MODULES
from BackEnd.backend import load_parameters

#LOAD PARAMETERS
parameters = load_parameters()

ASSETS_FILE_NAME = parameters["assets_file_name"]

im_heart: str = join('.', ASSETS_FILE_NAME, parameters["card_files_names"]["heart"])
im_clover: str = join('.', ASSETS_FILE_NAME, parameters["card_files_names"]["clover"])
im_shield: str = join('.', ASSETS_FILE_NAME, parameters["card_files_names"]["shield"])
im_coin: str = join('.', ASSETS_FILE_NAME, parameters["card_files_names"]["coin"])