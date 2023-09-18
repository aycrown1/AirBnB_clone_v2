#!/usr/bin/python3
""" New Engine """
from sqlalchemy import create_engine
from models.base_model import Base, BaseModel
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.review import Review
from models.amenity import Amenity
from sqlalchemy.orm import sessionmaker, scoped_session
from os import getenv


class DBStorage:
    """
    This class defines methods to interact with the MySQL database.
    The class serializes instances for database storage
    Attributes:
        __engine: engin to connect db
        __session: session to interact with db
    """
    __engine = None
    __session = None
    __classes = {'BaseModel': BaseModel,
                 'User': User,
                 'Place': Place,
                 'State': State,
                 'City': City,
                 'Amenity': Amenity,
                 'Review': Review
                 }

    def __init__(self):
        """
        Initializing the __engine
        """
        self.__engine = create_engine("mysql+mysqldb://{}:{}@{}/{}"
                                      .format(getenv('HBNB_MYSQL_USER'),
                                              getenv('HBNB_MYSQL_PWD'),
                                              getenv('HBNB_MYSQL_HOST'),
                                              getenv('HBNB_MYSQL_DB')),
                                      pool_pre_ping=True)
        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """query for objects depend on the class
        Args:
            cls: class to query
        """
        object = {}
        cls = cls if not isinstance(cls, str) else self.__classes.get(cls)
        if cls:
            for obj in self.__session.query(cls).all():
                key = "{}.{}".format(obj.__class__.__name__, obj.id)
                object[key] = obj
        else:
            for cls_name, cls in self.__classes.items():
                for obj in self.__session.query(cls).all():
                    key = "{}.{}".format(cls_name, obj.id)
                    object[key] = obj
        return object

    def new(self, obj):
        """add an object to current db session
        Args:
            obj: object to add
        """
        if obj:
            self.__session.add(obj)

    def save(self):
        """commit all changes of current db session
        """
        self.__session.commit()

    def delete(self, obj=None):
        """delete obj from current db session
        Args:
            obj: object to delete
        """
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """create all tables in the database
        """
        Base.metadata.create_all(self.__engine)
        factory = sessionmaker(bind=self.__engine, expire_on_commit=True)
        self.__session = scoped_session(factory)()

    def close(self):
        """remove current session and roll back all unsaved transactions
        """
        if self.__session:
            self.__session.close()
