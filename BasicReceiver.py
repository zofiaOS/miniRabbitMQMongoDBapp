import pika


def consume(queue, callback):
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost')
    )
    channel = connection.channel()
    channel.queue_declare(queue=queue)
    channel.basic_consume(callback,
                          queue=queue,
                          no_ack=True)
    channel.start_consuming()
