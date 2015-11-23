import HorseManager

from tests.BasicTest import BasicTest
from tests.BasicTest import TEST_DB
from tests.BasicTest import TEST_HORSE


WRONG_HORSE = 'tests/horses/wrong_one'
WRONG_DIR = 'tests/horses/wrong_dir'


class TestBasicDB(BasicTest):

    def testAddingHorse(self):
        # Add horse to the database
        HorseManager.add_horse_from_file(TEST_HORSE, TEST_DB)

        # Check if stormy is in the database
        self.is_horse_in_db(self.stormy)

    def testAddingWithWrongData(self):
        with self.assertRaises(ValueError):
            HorseManager.add_horse_from_file(WRONG_HORSE, TEST_DB)

    def testAddingFromWrongDir(self):
        with self.assertRaises(IOError):
            HorseManager.add_horse_from_file(WRONG_DIR, TEST_DB)
