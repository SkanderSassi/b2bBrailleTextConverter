from datetime import datetime
from common.exceptions import *
from werkzeug.utils import secure_filename


def get_secure_filename(filename):
    filename_secure = secure_filename(filename)
    if not filename_secure:
        raise EmptyFileName("Empty filename")
    return filename_secure


def check_filetype_allowed(filetype, allowed_types):
    if filetype not in allowed_types:
        raise FileTypeNotAllowed(
            f"The specified file type is not allowed, allowed file types : {allowed_types}",
            filetype,
        )

def create_timestamp(as_int = False):
    dt = datetime.now()
    ts = datetime.timestamp(dt)
    if as_int:
        return int(ts)
    return str(ts).replace('.','-')

