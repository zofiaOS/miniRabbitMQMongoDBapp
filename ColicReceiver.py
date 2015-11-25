import BasicReceiver
import HorseManager


def send_mail(mail, msg):
    # TODO function that will send mail to the owner
    pass


def callback(ch, method, properties, body):
    horse_id, database = body.split()
    try:
        Owner_mail = HorseManager.find_horse(horse_id, database)['Mail']
    except KeyError:
        print("Owners mail not known")
        raise
    send_mail(Owner_mail, "Your horse has colic!")
    ch.basic_ack(delivery_tag=method.delivery_tag)

# The message has to be durable and acknowledged
BasicReceiver.consume('colic_monitoring', callback, durable=True, no_ack=False)
