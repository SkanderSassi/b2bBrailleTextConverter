import os
import flaskapp

from pathlib import Path
from flask import request, make_response
from dotenv import load_dotenv
from config import load_config
from http import HTTPStatus as statuses
from common.utils import check_filetype_allowed, get_secure_filename
# 202 accepted and in prosesing
from common.exceptions import *

load_dotenv()

UPLOAD_DIR = os.environ['UPLOAD_DIR']

app = flaskapp.create_app()




@app.route('/upload', methods=['POST'])
def upload():
    #Refactor to try except
    file = request.files['file']
    try:
        filename = get_secure_filename(file.filename)
        file_type = file.mimetype.split('/')[-1]
        check_filetype_allowed(file_type)
        upload_path = Path(UPLOAD_DIR)
        upload_path.mkdir(parents=True, exist_ok=True)
        file.save(upload_path.joinpath(filename))
    except EmptyFileName as e:
        print(e.with_traceback())
        return make_response('Empty filename', statuses.BAD_REQUEST)
    except FileTypeNotAllowed as e:
        print(e.with_traceback())
        return make_response('File type not allowed', statuses.BAD_REQUEST)
    
    
    return make_response(f"File allowed in {upload_path}", statuses.OK)
        

    

if __name__ == '__main__':
    config = load_config()
    # import flaskapp.routes
    app.run(host=config.HOST_IP,port=config.PORT,debug=config.DEBUG)
    