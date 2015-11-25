import BasicReceiver
import HorseManager


def callback(ch, method, properties, body):
    horse_id, database, condition = body.split()
    HorseManager.modify_horse_doc(horse_id, database, 'Condition', condition)
    ch.basic_ack(delivery_tag=method.delivery_tag)

# The message has to be acknowledged
BasicReceiver.consume(
    '',
    callback,
    no_ack=False,
    exchange='emergency'
)
