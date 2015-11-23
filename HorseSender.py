import pika


def send_add_horse_request(msg, props):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost')
    )
    channel = connection.channel()
    channel.queue_declare(queue='adding_horses')
    channel.basic_publish(
        exchange='',
        routing_key='adding_horses',
        body=msg,
        properties=props
    )
    connection.close()
