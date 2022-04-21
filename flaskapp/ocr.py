import os
from xml.dom.minidom import Document
from doctr.models import ocr_predictor
from doctr.io import DocumentFile
from tools import pdf_to_image
from config import config


MODEL_MAP = {'VGG16' : 'crnn_vgg16_bn',
             'SAR': 'sar_resnet31',
             'MASTER' : 'master',
             'RESNET50' : 'db_resnet50',
             'RESNET50-RO': 'db_resnet50_rotation'
             }

class OCR():
    def __init__(self, det = MODEL_MAP['RESNET50'], rec = MODEL_MAP['VGG16'], 
                 doc_dir = '/upload',
                 tmp_dir = '/tmp', 
                 use_gpu = False,
                 verbose = False,
                 pretrained = False):
        self.detector = det
        self.recognizer = rec
        self.doc_dir = doc_dir
        self.tmp_dir = tmp_dir
        self.predictor = None
        self.use_gpu = use_gpu
        self.verbose = verbose
        self.pretrained = pretrained
        self.__start_ocr()
    def __start_ocr(self):
        if self.verbose:
            print("Starting OCR")
        self.predictor = ocr_predictor(det_arch=self.detector, 
                                  reco_arch=self.recognizer, 
                                  pretrained=self.pretrained, 
        )
        if self.use_gpu:
            self.predictor.cuda()
        else:
            self.predictor.cpu()
        if self.verbose:
            print("OCR started")
    def to_gpu(self, device_id = 'cuda:0'):
        # TODO add predictor not initialized here
        if self.predictor is None:
            pass
        if self.verbose:
            print("Switching OCR to GPU")
        self.predictor.cuda(device_id)
    def to_cpu(self):
        #TODO predictor not initialized
        if self.predictor is None:
            pass
        if self.verbose:
            print("Switching OCR to CPU")
        self.predictor.cpu()
    def extract(self, filename, is_rotated = False):
        # TODO add support for images
        if self.verbose:
            print(f"OCR launched on file {filename}")
        file_path = os.path.join(self.doc_dir,filename)
        print(file_path)
        self.predictor.assume_straight_pages = not is_rotated
        docfile = DocumentFile.from_pdf(file_path)
        output = self.predictor(docfile)
        if self.verbose:
            print(f"OCR finished on file {file_path}")
        return output
        
    def __prepare_data(self):
        pass


    
    
    
    