# 202 accepted and in prosesing
import os
import flaskapp
import json
from pathlib import Path
from flask import jsonify, request
from dotenv import load_dotenv
from config import config
from http import HTTPStatus as statuses
from common.utils import check_filetype_allowed, get_secure_filename, extract_lines,extract_hocr_lines
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
    print(config.USE_HOCR)
    ocr_output =  ocr.extract(data['filename'], use_hocr = config.USE_HOCR)
    if config.USE_HOCR:
        #TODO reformat this ugly code
        return jsonify([{'page_number': page_idx ,
                     'lines' : extract_hocr_lines(page, 
                                             config.MINIMUM_CONFIDENCE,                
                                             )}
                    for page_idx, page in enumerate(ocr_output)]), statuses.OK
    else:
        return jsonify([{'page_number': page['page_idx'] ,
                        'lines' : extract_lines(page, 
                                                config.MINIMUM_CONFIDENCE,
                                                )}
                        for page in ocr_output['pages']]), statuses.OK

@app.route('/cancel',methods=['POST'])
def cancel():
    pass
    
if __name__ == '__main__':
   
    # import flaskapp.routes
    app.run(host=config.HOST_IP,
            port=config.PORT,
            debug=config.DEBUG)
    