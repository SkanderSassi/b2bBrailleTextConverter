# 202 accepted and in prosesing
import os
import json
from http.client import BAD_REQUEST
from pathlib import Path
from flask import Response, jsonify, request,make_response
from dotenv import load_dotenv
from config import config
from http import HTTPStatus as statuses
from common.utils import extract_lines
from common.exceptions import *
from common.helpers import create_timestamp,check_filetype_allowed, get_secure_filename
from flaskapp.ocr import OCR
from flaskapp import create_app


load_dotenv()



app = create_app()




@app.route('/upload', methods=['POST'])
def upload():
    #Refactor to try except
    # print(request.files)
    file = request.files['file']
    try:
        filename = get_secure_filename(file.filename)
        file_type = file.mimetype.split('/')[-1]
        check_filetype_allowed(file_type, config.ALLOWED_TYPES)
        upload_path = Path(config.UPLOAD_DIR)
        upload_path.mkdir(parents=True, exist_ok=True)
        tstamp = create_timestamp(True)
        filename_with_stamp = f"{tstamp}{filename}"
        file.save(upload_path.joinpath(filename_with_stamp))
    except EmptyFileName as e:
        # print(e.with_traceback())
        return make_response(jsonify({'message':e.message})
                             , statuses.BAD_REQUEST)
    except FileTypeNotAllowed as e:
        # print(e.with_traceback())
        return make_response(jsonify({'message':e.message}), 
                             statuses.BAD_REQUEST)
    return make_response(jsonify({'message': 'File uploaded', 'filename': filename_with_stamp}), 
                         statuses.OK)
    
@app.route('/extract', methods=['POST'])
def extract():
    try:
        data = json.loads(request.data)
        ocr = OCR(doc_dir=config.UPLOAD_DIR, pretrained=True, verbose=True)
        ocr.to_gpu()
        print(f"Using HOCR : {config.USE_HOCR}")
        ocr_output =  ocr.extract(data['filename'], use_hocr = config.USE_HOCR)
    except FileNotFoundError as e:
        return make_response(jsonify({'message' : 'Uploaded file not found in server'}),
                                     statuses.BAD_REQUEST)
    except Exception as e:
        return make_response(jsonify({'message' : 'Something happened'}),statuses.INTERNAL_SERVER_ERROR)
    if config.USE_HOCR:
        #TODO reformat this ugly code
         return make_response(jsonify({'pages':[{'page_number': page_idx ,
                                 '      lines' : extract_lines(page, 
                                                        config.MINIMUM_CONFIDENCE,
                                                )} for page_idx ,page in enumerate(ocr_output)]
                         }
                        ), statuses.OK)
    else:
        return make_response(jsonify({'pages':[{'page_number': page['page_idx'] ,
                                      'lines' : extract_lines(page, 
                                                              config.MINIMUM_CONFIDENCE,
                                                )} for page in ocr_output['pages']]
                        }
                        ), statuses.OK)

@app.route('/cancel',methods=['POST'])
def cancel():
    pass
    
if __name__ == '__main__':
   
    # import flaskapp.routes
    app.run(host=config.HOST_IP,
            port=config.PORT,
            debug=config.DEBUG)
    