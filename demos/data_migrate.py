import sys 
sys.path.append("..") 
from tools import di

class Migrate():

    def source(self):
        pass
    
    def target(self):
        pass
    
    def _migrate(self):
        pass

    def get_source_data(self):
        self.data = []
        

    def exec(self):
        self.get_source_data()
        self._migrate()



m = Migrate()
m.exec()