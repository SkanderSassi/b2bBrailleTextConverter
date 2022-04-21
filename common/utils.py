from argparse import FileType
import os


from flask import g
from common.exceptions import *
from werkzeug.utils import secure_filename
from config import config


def get_secure_filename(filename):
    filename_secure = secure_filename(filename)
    if not filename_secure:
        raise EmptyFileName("Empty filename")
    return filename_secure

def check_filetype_allowed(filetype):
    print(config.ALLOWED_TYPES)
    if filetype not in config.ALLOWED_TYPES:
        raise FileTypeNotAllowed(f"The specified file type is not allowed, allowed file types : {config.ALLOWED_TYPES}", filetype)
