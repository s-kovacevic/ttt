import logging
from util import get_config
from tinydb import TinyDB, Query

database_config = get_config(section='DATABASE')
database = TinyDB(database_config['db_file'] or 'db.json')
logger = logging.getLogger(__name__)


class DatabaseMixin(object):
    """
    Mixin Class that allows easy relating between database and python objects.
    In order to use it, define class variable `__table__` and override
    to_database_object and from_database_object methods.
    """

    def __init__(self):
        super().__init__()
        try:
            self.table = database.table(self.__table__)
        except AttributeError as e:
            raise Exception(
                'Define `__table__` class variable if you want to use'
                'DatabaseMixin'
            ) from e

    def to_database_object(self):
        """
        Convert your object to dict representation, that will be saved to
        database.
        :return: dictionary of what you want to be persisted in database
        """
        raise NotImplementedError

    @staticmethod
    def from_database_object(db_object):
        """
        Implementation should create python class instance from the dictionary
        fetched from the database.
        :param db_object: dictionary fetched from the database
        :return: python object instance
        """
        raise NotImplementedError

    def persist(self):
        """
        Upserts the object to the database.
        """
        db_object = self.to_database_object()
        logger.debug('Upserting object: {} into table {}'.format(
            str(db_object), self.__table__
        ))
        self.table.upsert(db_object, Query()['id_'] == db_object['id_'])

    @classmethod
    def load_from_database(cls, id_):
        """
        Loads object from database and creates appropriate python class
        instance. Pretty hacky, but fun.
        :param id_: UUID of the object you want to load from database
        :return: loaded object instance or None if UUID could not be found in
        database
        """
        results = database.table(cls.__table__).search(Query()['id_'] == id_)
        if results:
            return cls.from_database_object(results.pop())
