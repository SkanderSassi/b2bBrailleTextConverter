from argparse import FileType
import os

from common.exceptions import *
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

load_dotenv()
ALLOWED_TYPES = set(os.environ['ALLOWED_TYPES'].split(','))



def get_secure_filename(filename):
    filename_secure = secure_filename(filename)
    if not filename_secure:
        raise EmptyFileName("Empty filename")
    return filename_secure

def check_filetype_allowed(filetype):
    print(ALLOWED_TYPES)
    if filetype not in ALLOWED_TYPES:
        raise FileTypeNotAllowed("The specified file type is not allowed", filetype)
