from doctr.models import ocr_predictor
from doctr.io import DocumentFile
import os

MODEL_MAP = {'VGG16' : 'crnn_vgg16_bn',
             'SAR': 'sar_resnet31',
             'MASTER' : 'master',
             'RESNET50' : 'db_resnet50',
             'RESNET50-RO': 'db_resnet50_rotation'
             }

def predict():
    detector = MODEL_MAP.get(os.environ['DET_ARCH'], 'db_resnet50')
    recognizer = MODEL_MAP.get(os.environ['REC_ARCH'], 'crnn_vgg16_bn')
    print(detector, recognizer)
    # predictor = ocr_predictor(pretrained=True)
    # docfile = DocumentFile.from_pdf(file='./datasets/documents/visa_document.pdf')
    # result = predictor(docfile)
    
if __name__ == '__main__':
    predict()