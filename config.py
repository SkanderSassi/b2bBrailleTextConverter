import os
from attr import attrs
from dotenv import load_dotenv



class Config():
    def __init__(self):
        
        self.API_KEY = os.environ['API_KEY']
        self.HOST_IP = os.environ['HOST_IP']
        self.PORT = os.environ['PORT']
    def __repr__(self) -> str:
        attrs = vars(self)
        return ', '.join("%s: %s" % item for item in attrs.items())
class DebugConfig(Config):
    def __init__(self):
        Config.__init__(self)
        self.DEBUG = True
        
class ProductionConfig(Config):
    def __init__(self):
        Config.__init__(self)
        self.DEBUG = False
    

def load_config() -> Config:
    load_dotenv()
    debug_enable = os.environ['DEBUG']
    if debug_enable == 'TRUE':
        return DebugConfig()
    return ProductionConfig()

