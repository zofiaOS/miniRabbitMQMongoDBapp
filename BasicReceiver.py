import pika


def consume(queue, callback, durable=False, no_ack=True, exchange=None):
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost')
    )
    channel = connection.channel()
    if exchange:
        channel.exchange_declare(exchange=exchange, type='fanout')
        queue = channel.queue_declare().method.queue
        channel.queue_bind(exchange=exchange, queue=queue)
    else:
        channel.queue_declare(queue=queue, durable=durable)
    channel.basic_consume(callback,
                          queue=queue,
                          no_ack=no_ack)
    channel.start_consuming()
