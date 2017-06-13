import unittest

from pymongo import MongoClient
from pymongo.database import Database

from sqltomongo.database import DatabaseConnection


class TestComparisons(unittest.TestCase):
    db = 'test'
    database = DatabaseConnection(db)
    empty_database = DatabaseConnection()
    client = MongoClient()

    def test_database_instance(self):
        self.assertEqual(isinstance(self.database.database, type(Database(self.client, self.db))), True)

    def test_database_name(self):
        self.assertEqual(self.database.database.name, self.db)
        # msg = '"another_db" is not in database names! Please check the name of '
        #           'database!'
        # self.assertRaises(ValueError, DatabaseConnection(''), self.db)

    def test_database_use_db(self):
        self.empty_database.use_db(self.db)
        self.assertEqual(self.empty_database.database.name, self.db)

        msg = '"another_db" is not in database names! Please check the name of database!'
        self.assertRaises(ValueError, self.empty_database.use_db('another_db'), msg)

    def test_database_authenticate(self):
        without_db = 'At first you must connect to the database with use method!'
        database = DatabaseConnection()
        self.assertRaises(ValueError, database.authenticate('user', 'passwd'), without_db)


if __name__ == '__main__':
    unittest.main()
