#!/usr/bin/python3
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.base_model import BaseModel, Base
from os import getenv
from sqlalchemy.orm import scoped_session
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


envi = getenv('HBNB_ENV')
user = getenv('HBNB_MYSQL_USER')
passwd = getenv('HBNB_MYSQL_PWD')
host = getenv('HBNB_MYSQL_HOST')
db = getenv('HBNB_MYSQL_DB')
str_type = getenv('HBNB_TYPE_STORAGE')

class DBStorage():
    """A database storage engine"""
    __engine = None
    __session = None

    def __init__(self):
        """An instantateous"""
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.format(user, passwd, host, db), pool_pre_ping=True)

        if envi == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Query on the current database session"""
        if cls is None:
            objs_query = self.__session.query(State).all()
            objs_query.extend(self.__session.query(City).all())
            objs_query.extend(self.__session.query(User).all())
            objs_query.extend(self.__session.query(Place).all())
            objs_query.extend(self.__session.query(Review).all())
            objs_query.extend(self.__session.query(Amenity).all())
        else:
            if type(cls) == str:
                cls = eval(cls)
            objs_query = self.__session.query(cls)
        return {"{}.{}".format(type(objt).__name__, objt.id):
                objt for objt in objs_query}

    def new(self, obj):
        """Adds new object to the db"""
        self.__session.add(obj)

    def save(self):
        """Commits the changes"""
        self.__session.commit()

    def delete(self, obj=None):
        """Deletes an obj from db"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Reloads all object and opens a comnection"""
        #Base.metadata.create_all(self.__engine)
        #sess = sessionmaker(bind=some_engine, expire_on_commit=False)
        #self.__session = scoped_session(sess)
        Base.metadata.create_all(self.__engine)
        Session = scoped_session(sessionmaker(bind=self.__engine,
                                              expire_on_commit=False))
        self.__session = Session()

    def close(self):
        """call remove() method on the private session attribute """
        self.__session.close()
