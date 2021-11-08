import pika, os, uuid, json
from flask import Flask
from dotenv import load_dotenv

app = Flask(__name__)

# loads env variables
load_dotenv()

class MapsRpcClient(object):

    def __init__(self):

        self.url = os.getenv('CLOUDAMQP_URL')
        self.params = pika.URLParameters(self.url)
        self.connection = pika.BlockingConnection(self.params)

        self.channel = self.connection.channel()

        result = self.channel.queue_declare('', exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, n):
        print("[x] Sent: " + n)
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key='get_map',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=n
        )
        while self.response is None:
            self.connection.process_data_events()
        print("[x] Response received: ")
        print(json.loads(self.response))

        self.connection.close()

        return json.loads(self.response)


@app.route('/')
def index():
    return 'OK'

@app.route('/get_map/<msg>')
def get_payload(msg):

    maps_rpc = MapsRpcClient()
    response = maps_rpc.call(msg.replace("'", '"'))
    return response

if __name__ == '__main__':
    app.run()