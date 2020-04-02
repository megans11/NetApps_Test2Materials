import pika
import json

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='Adder')

def callback(ch, method, properties, body):
	print(" [x] Received %r" % json.loads(body))
	the_sum = 0
	for i in json.loads(body):
		the_sum = the_sum + i
	print(" Computed sum %r" % str(the_sum))
	
channel.basic_consume(queue='Adder',
						auto_ack=True,
						on_message_callback=callback)
						
print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
