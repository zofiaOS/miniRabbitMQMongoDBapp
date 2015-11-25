import pika


def _send_msg(msg, queue, props={}, durable=False):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost')
    )
    channel = connection.channel()
    channel.queue_declare(queue=queue, durable=durable)
    channel.basic_publish(
        exchange='',
        routing_key=queue,
        body=msg,
        properties=props
    )
    connection.close()


def send_add_horse_request(msg, props):
    _send_msg(msg, 'adding_horses', props)


def send_collic_msg(msg):
    # We want the msg to be durable and persistent so it's not lost
    _send_msg(
        msg,
        'colic_monitoring',
        pika.BasicProperties(delivery_mode=2),  # msg is persistent
        durable=True
    )
