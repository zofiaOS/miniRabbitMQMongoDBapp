import pika


def consume(queue, callback, durable=False, no_ack=True):
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost')
    )
    channel = connection.channel()
    channel.queue_declare(queue=queue, durable=durable)
    channel.basic_consume(callback,
                          queue=queue,
                          no_ack=no_ack)
    channel.start_consuming()
