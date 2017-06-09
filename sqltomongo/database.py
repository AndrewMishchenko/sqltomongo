import sys

from pymongo import MongoClient
from pymongo.database import Database
from pymongo.errors import ServerSelectionTimeoutError, OperationFailure


class DatabaseConnection(object):
    def __init__(self, database=None, host='localhost', port=27017):
        """Establish the connection with the mongo backend"""

        self.timeout = 1
        self.host = str(host)
        if not isinstance(port, int):
            raise ValueError('Entered port is "{}"! Must be integer type'.
                             format(port))
        self.port = port
        self.client = MongoClient(host=self.host,
                                  port=self.port,
                                  serverSelectionTimeoutMS=self.timeout)
        try:
            if database is not None:
                if database in self.client.database_names():
                    self.database = Database(self.client, database)
                    if self.database.command("serverStatus")['ok'] == 1.0:
                        print('connecting to: mongodb://{}:{}'.format(
                            self.host, self.port))
                        print('database - "{}"'.format(self.database.name))
                    else:
                        pass

                else:
                    raise ValueError
            else:
                self.database = database

        except ServerSelectionTimeoutError as err:
            sys.exit('Error! {}'.format(err))
        except ValueError:
            print('"{}" is not in database names! Please check the name of '
                  'database!'.format(database))

    def use_db(self, database=None):
        try:
            if database in self.client.database_names():
                self.database = Database(self.client, database)
                print('switched to db {}'.format(self.database.name))
            else:
                raise ValueError
        except ServerSelectionTimeoutError as err:
            sys.exit('Error! {}'.format(err))
        except ValueError:
            print('"{}" is not in database names! Please check the name of '
                  'database!'.format(database))

    def authenticate(self, user=None, password=None):
        if user is not None and password is not None:
            try:
                if user in [user['user'] for user in (
                        self.database.command('usersInfo')
                )['users']]:
                    try:
                        if self.database.authenticate(user, password):
                            self.auth = self.database.authenticate(user,
                                                                   password)
                            print('1')
                        else:
                            raise OperationFailure
                    except OperationFailure:
                        print('Error: Authentication failed.')
                        print('0')
                else:
                    print('"{}" user is not in "{}" database users!'.format(
                        user, self.database.name))
            except AttributeError:
                print('At first you must connect to the database with use '
                      'method!')
        else:
            print('Please check entered user and password!')
