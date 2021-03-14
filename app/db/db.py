from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker


class MetaSingleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(MetaSingleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class DBConnector(metaclass=MetaSingleton):
    session = None
    connection = None

    def connect(self):
        if self.session is None:
            engine = create_engine('postgresql+psycopg2://miem:Vladimir33!@51.15.104.77:5432/graders')
            self.connection = engine.connect()
            Session = sessionmaker()
            Session.configure(bind=self.connection)
            self.session = Session()
        return self.session
