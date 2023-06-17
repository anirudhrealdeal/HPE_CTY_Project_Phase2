import pika, json, os, django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "admin.settings")
django.setup()

from products.models import Product

# this paclage helps us send events
params = pika.URLParameters('amqps://mtfsepje:kh6Q1ds6NHfH8WNoCc7MqBdedgUPI4Np@rat.rmq2.cloudamqp.com/mtfsepje')
connection = pika.BlockingConnection(params)
channel = connection.channel()

channel.queue_declare(queue='admin')

def callback(ch, method, properties, body):
    print('Recieved in admin')
    id = json.loads(body)
    print(id)
    product = Product.objects.get(id=id)
    product.likes = product.likes+1
    product.save()
    print('Product likes increased!')

channel.basic_consume(queue='admin', on_message_callback=callback, auto_ack=True)
print('Started Consuming...')
channel.start_consuming()
channel.close()
