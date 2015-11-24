import pika


def _send_msg(msg, queue, props={}):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost')
    )
    channel = connection.channel()
    channel.queue_declare(queue=queue)
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
    _send_msg(msg, 'colic_monitoring')
