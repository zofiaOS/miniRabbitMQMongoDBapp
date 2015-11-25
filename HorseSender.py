import pika


def _send_msg(msg, queue, props={}, durable=False, exchange=''):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost')
    )
    channel = connection.channel()
    if exchange:
        channel.exchange_declare(exchange=exchange, type='fanout')
    else:
        channel.queue_declare(queue=queue, durable=durable)
    channel.basic_publish(
        exchange=exchange,
        routing_key=queue,
        body=msg,
        properties=props
    )
    connection.close()


def send_add_horse_request(msg, props):
    _send_msg(msg, 'adding_horses', props)


def send_emergency_msg(msg):
    # We want the msg to be persistent so it's not lost
    _send_msg(
        msg,
        '',
        pika.BasicProperties(delivery_mode=2),  # msg is persistent
        exchange='emergency'
    )
