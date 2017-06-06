from pymongo import MongoClient

from sqltomongo.exceptions import SqmongoConnectionError


class DatabaseConnect(object):
    """Initializes the connection to the database."""

    def __init__(self, db=None):
        """
        :param db: The name of database
        """
        try:
            if db is None:
                raise SqmongoConnectionError(db)
        except SqmongoConnectionError:
            pass
        else:
            self.db = str(db)
            self.client = MongoClient()

    def _connection(self):
        return self.client[self.db]
