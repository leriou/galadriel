import pymysql as mysql

conn = mysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123456')
cur = conn.cursor()
sql = "select * from jike.t limit 10"
cur.execute(sql)
res = cur.fetchall()
print(res)
