# Google Maps Microservice

This is a google maps microservice that returns a URL to be used to embed a map
based on a location to your website. It uses RabbitMQ and CloudAMQP to handle 
messages between applications, and a flask server to host RabbitMQ. The service
is hosted on Heroku.

## How to use:
The test.py file in the main subdirectory has the code that demonstrates use.

To call the service, prepare JSON formatted **data** in the form of: `{"location": 
"destination"}`. 

Then add the prepared **data** to the following URL:
`https://map-microservice.herokuapp.com/get_map/"your data here"` without the quotations.

The service will return a JSON formatted dictionary with the map embed URL. There 
are various ways to retrieve this data.

### Python example on how to retrieve data:
```
import requests, json

call = "https://map-microservice.herokuapp.com/get_map/{"location": "Grand Canyon National Park, Arizona"}

response = json.dumps(requests.get(call).json())

# this would return {"url": "requested url here", "success": "true"}