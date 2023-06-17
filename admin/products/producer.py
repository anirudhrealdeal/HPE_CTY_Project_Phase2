# amqps://mtfsepje:kh6Q1ds6NHfH8WNoCc7MqBdedgUPI4Np@rat.rmq2.cloudamqp.com/mtfsepje
import pika, json
# this paclage helps us send events
params = pika.URLParameters('amqps://mtfsepje:kh6Q1ds6NHfH8WNoCc7MqBdedgUPI4Np@rat.rmq2.cloudamqp.com/mtfsepje')
connection = pika.BlockingConnection(params)
channel = connection.channel()

def publish(method, body):
    properties = pika.BasicProperties(method)

    channel.basic_publish(exchange='', routing_key='main', body=json.dumps(body), properties=properties )