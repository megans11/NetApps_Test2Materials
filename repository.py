import sys
import pymongo
import time
from datetime import datetime
import pika

# start a RabbitMQ channel
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# start MongoDB
client = pymongo.MongoClient()
db = client.test

looping = True
while looping:
	# get keyboard entered command
	command = input("Enter command: ")

	# get time for checkpoint 1
	dateTimeObj = datetime.now()
	timeObj = dateTimeObj.time()
	print('[Checkpoint 01:', timeObj, '] Message captured: ', command)

	# create a dictionary for the parsed command
	commandDict = {}
	if command[0:2] == 'p:':
		commandDict['type'] = 'produce'
	elif command[0:2] == 'c:':
		commandDict['type'] = 'consume'
	elif command == "quit":
		looping = False
		break
	else:
		print("Wrong format")
		
	if command.index('+') != -1: 
		# Get place
		place = command[command.index(':')+1:command.index('+')]
		commandDict['place'] = place

	if commandDict['type'] == 'produce':
		subject = command[command.index('+')+1:command.index('"')-1] # Get subject
		message = command[command.index('"'):] # Get message
		commandDict['subject'] = subject
		commandDict['message'] = message
	elif commandDict['type'] == 'consume':
		subject = command[command.index('+')+1:]
		commandDict['subject'] = subject
		commandDict['message'] = "n/a"

	# create mongo document
	msgID = "17$" + str(time.time())
	if commandDict['type'] == 'produce':
		mongoDocument = {
			"Action": "p",
			"Place": commandDict['place'],
			"MsgID": msgID, 
			"Subject": commandDict['subject'], 
			"Message": commandDict['message'] }	
	elif commandDict['type'] == 'consume':
		mongoDocument = {
			"Action": "c",
			"Place": commandDict['place'],
			"MsgID": msgID, 
			"Subject": commandDict['subject'], 
			"Message": commandDict['message'] }	
			
	# insert mongo document
	db.utilization.insert(mongoDocument)
			
	# get time for checkpoint 2
	dateTimeObj = datetime.now()
	timeObj = dateTimeObj.time()
	print('[Checkpoint 02:', timeObj, '] Store command in MongoDB instance: ', mongoDocument)

	# RabbitMQ
	if commandDict['type'] == 'produce':
		# if produce, publish message in RabbitMQ
		channel.basic_publish(exchange=commandDict['place'], 
							routing_key=commandDict['subject'],
							body=commandDict['message'])
		# get time for checkpoint 3
		dateTimeObj = datetime.now()
		timeObj = dateTimeObj.time()
		print("[Checkpoint 03:", timeObj, "] Message sent: ", 
					"%s:%s:%s:" % (commandDict['place'], commandDict['subject'], commandDict['message']))
							
	elif commandDict['type'] == 'consume':
		# if consume, bind and wait for a consumed message in RabbitMQ
		channel.queue_bind(exchange=commandDict['place'],
							queue=commandDict['subject'],
							routing_key=commandDict['subject'])
		def callback(ch, method, properties, body):
			# get time for checkpoint 3
			dateTimeObj = datetime.now()
			timeObj = dateTimeObj.time()
			print("[Checkpoint 03:", timeObj, "] Message captured: ", "%r:%s" % (method.routing_key, str(body, 'utf-8')))
			
		print(commandDict['subject'])
		channel.basic_consume(queue=commandDict['subject'], on_message_callback=callback, auto_ack=True)
		channel.start_consuming()

