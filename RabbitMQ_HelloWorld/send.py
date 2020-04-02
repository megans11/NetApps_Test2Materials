import pika
import json

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

my_list = [1, 2, 3, 4 ,5]

channel.queue_declare(queue='Adder')
channel.basic_publish(exchange='',
						routing_key='Adder',
						body=json.dumps(my_list))
print(" [x] Send list body")
connection.close()
