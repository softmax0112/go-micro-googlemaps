import pika, json, os
from dotenv import load_dotenv

# loads env variables
load_dotenv()

url = os.getenv('CLOUDAMQP_URL')

params = pika.URLParameters(url)
connection = pika.BlockingConnection(params)
channel = connection.channel()
channel.queue_declare(queue='get_map')

def is_json(entry):
    '''
    Function that detects if passed body is in JSON format
    '''

    try:
        json.loads(entry)
    except:
        return False

    return True

def call_maps_api(location):
    '''
    Function that calls the Google Maps API to get a response
    '''

    formatted = location.replace(", ", ",", 1).replace(", ", " ").replace(" ", "+")


    api_key = os.getenv('API_KEY')

    embed_url = 'https://www.google.com/maps/embed/v1/' + 'place' + '?key=' + api_key + '&q=' + formatted

    return embed_url

def on_request(ch, method, props, body):

    print(is_json(body))

    if is_json(body):
        request = json.loads(body)

        if 'location' in request:
            response = {"url": call_maps_api(request['location'])}
            response["success"] = True
            response = json.dumps(response)

            print("[x] Sending the following response back: ")
            print(response)
        else:
            response = json.dumps({"success": False, "error": "Incorrect JSON format"})

    else:
        response = json.dumps({"success": False, "error": "Incorrect format"})

    ch.basic_publish(exchange = '',
                  routing_key = props.reply_to,
                  properties = pika.BasicProperties(correlation_id = \
                                  props.correlation_id),
                  body=json.dumps(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='get_map',
                      on_message_callback=on_request,
                        )

print(" [x] Awaiting RPC Requests")
channel.start_consuming()
connection.close()