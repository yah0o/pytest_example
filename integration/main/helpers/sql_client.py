from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

from integration.main.logger import log


class SqlClient(object):
    class DbType(object):
        MYSQL = 'mysql'
        POSTGRESQL = 'postgresql'

    def __init__(self, host, port, db_name, user, password, db_type=DbType.MYSQL):
        self.__url = '{}://{}:{}@{}:{}/{}'.format(db_type, user, password, host, port, db_name)
        self.__engine = None
        self.__connection = None

    @property
    def connection(self):
        """
        :return: 
        """

        return self.__connection

    def connect(self):
        """
        :return: None
        """

        if self.__engine is None:
            self.__engine = create_engine(self.__url)

        if self.__connection is None:
            try:
                self.__connection = self.__engine.connect()
                log.info('Connected to DB successfully')
            except SQLAlchemyError, e:
                log.error(e)

    def execute(self, query, **kwargs):
        """
        :param query: 
        :param kwargs: 
        :return: 
        """

        try:
            rows = self.connection.execute(text(query), **kwargs).fetchall()
            log.info('Operation completed successfully')
            return rows
        except SQLAlchemyError as e:
            log.error(e)
            return []

    def disconnect(self):
        """
        :return: 
        """

        if self.__connection:
            try:
                self.__connection.close()
                self.__connection = None
                log.info('Connection to DB closed successfully')
            except SQLAlchemyError as e:
                log.error(e)
