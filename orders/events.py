import json
import pika

def send_event_to_broker(event_name, payload):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='events_queue')

    event = {
        "event_name": event_name,
        "payload": payload
    }
    channel.basic_publish(
        exchange='',
        routing_key='events_queue',
        body=json.dumps(event)
    )
    connection.close()
