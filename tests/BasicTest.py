import unittest

from pymongo import MongoClient


TEST_DB = 'test_db'
TEST_HORSE = 'tests/horses/stormy'


class BasicTest(unittest.TestCase):

    def setUp(self):
        # Destroy former test databases
        self.client = MongoClient()
        if TEST_DB in self.client.database_names():
            self.client.drop_database(TEST_DB)
        self.stormy = {'Name': 'Stormy', 'Owner': 'Jack'}

    def is_horse_in_db(self, horse):
        db = self.client[TEST_DB]
        horses = db.horses
        document = horses.find_one({'Name': 'Stormy'})
        for k in horse:
            self.assertEqual(horse[k], document[k])
