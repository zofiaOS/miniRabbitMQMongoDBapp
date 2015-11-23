import pika
import subprocess

import HorseManager
import HorseSender

from tests.BasicTest import BasicTest
from tests.BasicTest import TEST_DB
from tests.BasicTest import TEST_HORSE


TIME_TO_ADD_HORSE = 1
TIMEOUT = 3


class TestHorseQueue(BasicTest):

    def _on_response(self, ch, method, props, body):
        if body == 'True':
            self.isAdded = True

    def _on_timeout(self):
        # On timeout check if receiver added horse to the database
        self.assertTrue(self.isAdded, msg="The horse document wasn't added")

    def setUp(self):
        super(TestHorseQueue, self).setUp()
        # Launch receiver
        self.receiver = subprocess.Popen(['python', 'HorseReceiver.py'])
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost')
        )

    def testAddingHorseThrougQueue(self):
        # Create queue to receive response from receiver
        channel = self.connection.channel()
        isAdded = channel.queue_declare(exclusive=True)
        self.callback_queue = isAdded.method.queue
        channel.basic_consume(
            self._on_response,
            no_ack=True,
            queue=self.callback_queue
        )
        self.isAdded = False

        # Send request through RabbitMQ to add a horse to test_database
        msg = TEST_HORSE + " " + TEST_DB
        # In props there is info on which queue to reply to
        props = pika.BasicProperties(reply_to=self.callback_queue)
        HorseSender.send_add_horse_request(msg, props)

        # Set timeout and wait for response
        self.connection.add_timeout(TIMEOUT, self._on_timeout)
        while not self.isAdded:
            self.connection.process_data_events()

        # Check if stormy is in the database
        self.is_horse_in_db(self.stormy)

    def tearDown(self):
        # Close connection
        self.connection.close()
        # Terminate the receiver process
        self.receiver.terminate()
