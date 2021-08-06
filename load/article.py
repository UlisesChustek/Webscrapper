from sqlalchemy import Column, String, Integer
from base import Base

class Article(Base):
    __tablename__ = 'articles'

    id = Column(String, primary_key=True)
    body = Column(String)
    #host = Column(String)
    n_tokens_body = Column(Integer)
    title = Column(String)
    n_tokens_title = Column(Integer)
    newspaper_uid = Column(String)
    url = Column(String, unique=True)

    def __init__(self,
                 uid,
                 body,
                 #host,
                 n_tokens_body,
                 title,
                 n_tokens_title,
                 newspaper_uid,
                 url):
        self.id = uid
        self.body = body
       # self.host = host
        self.newspaper_uid = newspaper_uid
        self.n_tokens_body = n_tokens_body
        self.n_tokens_title = n_tokens_title
        self.title = title
        self.url = url