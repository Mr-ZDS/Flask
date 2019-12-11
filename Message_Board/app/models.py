from datetime import datetime
from app import db

#保存留言的Message模型
class Message(db.Model):
    id=db.Column(db.Integer,primary_key = True)
    body=db.Column(db.String(200))
    name=db.Column(db.String(20))
    timestamp=db.Column(db.DateTime,default = datetime.utcnow,index = True)     #存储每一条留言的发表时间