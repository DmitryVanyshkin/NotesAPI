from .db import DBConnector


class QueryProcessor:

    def __init__(self):
        connector = DBConnector()
        self.session = connector.connect()
        self.connection = connector.connection

    def findEntity(self, key, value, cls):
        return self.session.query(cls).filter(getattr(cls, key) == value).scalar()

    def addEntity(self, table_obj):
        self.session.add(table_obj)
        self.session.commit()
