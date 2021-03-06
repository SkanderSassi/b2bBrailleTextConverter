import os
from attr import attrs
from dotenv import load_dotenv



class Config():
    def __init__(self):
        
        self.API_KEY = os.environ['API_KEY']
        self.HOST_IP = os.environ['HOST_IP']
        self.PORT = os.environ['PORT']
        self.UPLOAD_DIR = os.environ['UPLOAD_DIR']
        self.TEMP_IMG_DIR= os.environ['TEMP_IMG_DIR']
        self.ALLOWED_TYPES = set(os.environ['ALLOWED_TYPES'].split(','))
        self.UPLOAD_DIR = os.environ['UPLOAD_DIR']
        self.MINIMUM_CONFIDENCE = float(os.environ['MINIMUM_CONFIDENCE'])
        self.USE_HOCR = os.environ['USE_HOCR'] == "TRUE"
    def __repr__(self) -> str:
        attrs = vars(self)
        return ', '.join("%s: %s" % item for item in attrs.items())
class DevelopmentConfig(Config):
    def __init__(self):
        Config.__init__(self)
        self.DEBUG = True
        
class ProductionConfig(Config):
    def __init__(self):
        Config.__init__(self)
        self.DEBUG = False
    

def load_config() -> Config:
    load_dotenv()
    env = os.environ['FLASK_ENV']
    if env == 'production':
        return ProductionConfig()
    return DevelopmentConfig()

config = load_config()