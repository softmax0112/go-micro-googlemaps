import requests, json

def is_json(entry):
    '''
    Function that detects if passed body is in JSON format
    '''

    try:
        json.loads(entry)
    except:
        return False

    return True

send_msg = {"location": "The Louvre, Paris, France"}

# call_service = "http://127.0.0.1:5000/get_map/" + str(send_msg)

call_service = "https://map-microservice.herokuapp.com/get_map/" + str(send_msg)

answer = json.dumps(requests.get(call_service).json())

if __name__ == '__main__':
    print(answer)
    print(is_json(answer))

