import subprocess

import HorseManager
import HorseSender

from tests.BasicTest import BasicTest
from tests.BasicTest import TEST_DB
from tests.BasicTest import TEST_HORSE


class TestHorseColic(BasicTest):

    def setUp(self):
        super(TestHorseColic, self).setUp()
        # Launch receivers
        self.receiver = subprocess.Popen(['python', 'EmergencyReceiver.py'])
        self.vetReceiver = subprocess.Popen(['python', 'VetEmergency.py'])
        # Add a horse to db
        HorseManager.add_horse_from_file(TEST_HORSE, TEST_DB)

    def testColicMsg(self):
        # Find a horses id
        horses = self.client[TEST_DB].horses
        horse_id = horses.find_one({'Name': self.stormy['Name']})['_id']

        # Send a msg that a horse has colic
        msg = str(horse_id) + " " + TEST_DB + " colic"
        HorseSender.send_emergency_msg(msg)

    def tearDown(self):
        # Terminate the receivers processes
        self.receiver.terminate()
        self.vetReceiver.terminate()
