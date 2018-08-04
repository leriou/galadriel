import pymysql as mysql


class MysqlManager():

    def __init__(self):
        self.cli = mysql.connect(host='127.0.0.1', port=3306, user='root', passwd='password')
        self.cursor  =  self.cli.cursor()


    def test(self):
        pass