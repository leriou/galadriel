import sys 
sys.path.append("..") 
from tools import di
import time


class S:

    def init(self):
        self.es = di.Di.getElasticsearch()
        
    
    def run(self):
        pass