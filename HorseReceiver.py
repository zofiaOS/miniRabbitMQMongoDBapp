import pika

import HorseManager

connection = pika.BlockingConnection(pika.ConnectionParameters(
    host='localhost')
)
channel = connection.channel()

channel.queue_declare(queue='adding_horses')

print ' [*] Waiting for messages. To exit press CTRL+C'


def callback(ch, method, properties, body):
    horse_dir, database = body.split()
    HorseManager.add_horse_from_file(horse_dir, database)
    ch.basic_publish(exchange='',
                     routing_key=properties.reply_to,
                     body='True')
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_consume(callback,
                      queue='adding_horses',
                      no_ack=True)

channel.start_consuming()
