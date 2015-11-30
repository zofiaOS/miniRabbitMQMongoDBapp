import HorseManager

from tests.BasicTest import BasicTest
from tests.BasicTest import TEST_DB
from tests.BasicTest import TEST_HORSE


WRONG_HORSE = 'tests/horses/wrong_one'
WRONG_DIR = 'tests/horses/wrong_dir'
MAGGIE = 'tests/horses/maggie'
BLUE = 'tests/horses/blue'
MISTY = 'tests/horses/misty'


class TestGroupConditions(BasicTest):

    def setUp(self):
        super(TestGroupConditions, self).setUp()
        HorseManager.add_many_horses([MAGGIE, MISTY, BLUE, TEST_HORSE], TEST_DB)

    def testGroupingByCondition(self):
        condition_horses = HorseManager.groupByCondition(TEST_DB)
        for ch in condition_horses:
            if ch['_id'] == None:
                self.assertIn(u'Stormy', ch['value']['horses'])
            if ch['_id'] == 'colic':
                self.assertIn(u'Misty', ch['value']['horses'])
            if ch['_id'] == 'heaves':
                self.assertEqual(len(ch['value']['horses']), 2)
