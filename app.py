# 202 accepted and in prosesing
import os
import flaskapp
import json
from pathlib import Path
from flask import jsonify, request
from dotenv import load_dotenv
from config import config
from http import HTTPStatus as statuses
from common.utils import check_filetype_allowed, get_secure_filename
from common.exceptions import *
from flaskapp.ocr import OCR
load_dotenv()



app = flaskapp.create_app()




@app.route('/upload', methods=['POST'])
def upload():
    #Refactor to try except
    file = request.files['file']
    try:
        filename = get_secure_filename(file.filename)
        file_type = file.mimetype.split('/')[-1]
        check_filetype_allowed(file_type)
        upload_path = Path(config.UPLOAD_DIR)
        upload_path.mkdir(parents=True, exist_ok=True)
        file.save(upload_path.joinpath(filename))
    except EmptyFileName as e:
        # print(e.with_traceback())
        return jsonify({'message':e.message}), statuses.BAD_REQUEST
    except FileTypeNotAllowed as e:
        # print(e.with_traceback())
        return jsonify({'message':e.message}), statuses.BAD_REQUEST
    return jsonify({'message': 'File uploaded'}), statuses.OK
        
@app.route('/extract', methods=['POST'])
def extract():
    data = json.loads(request.data)
    ocr = OCR(doc_dir=config.UPLOAD_DIR, pretrained=True, verbose=True)
    ocr.to_gpu()
    result =  ocr.extract('visa_document.pdf')
    print(result)
    return jsonify({'message': 'Text Extraction successfull'}), statuses.ACCEPTED

@app.route('/cancel',methods=['POST'])
def cancel():
    pass
    

if __name__ == '__main__':
   
    # import flaskapp.routes
    app.run(host=config.HOST_IP,
            port=config.PORT,
            debug=config.DEBUG)
    