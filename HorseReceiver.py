import BasicReceiver
import HorseManager


def callback(ch, method, properties, body):
    horse_dir, database = body.split()
    HorseManager.add_horse_from_file(horse_dir, database)
    ch.basic_publish(exchange='',
                     routing_key=properties.reply_to,
                     body='True')
    ch.basic_ack(delivery_tag=method.delivery_tag)


BasicReceiver.consume('adding_horses', callback)
