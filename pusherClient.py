import pysher
import json
import time

# Add a logging handler so we can see the raw communication data
# import logging
# root = logging.getLogger()
# root.setLevel(logging.INFO)
# ch = logging.StreamHandler(sys.stdout)
# root.addHandler(ch)

pusher = pysher.Pusher('145a8e68bfa0d0947608','us2',True)

def  my_func(*args, **kwargs):
    print(json.loads(args, indent=4, sort_keys=True))

# We can't subscribe until we've connected, so we use a callback handler
# to subscribe when able
def connect_handler(data):
    channel = pusher.subscribe('my-channel')
    channel.bind('my-event', my_func)

pusher.connection.bind('pusher:connection_established', connect_handler)
pusher.connect()

while True:
    # Do other things in the meantime here...
    time.sleep(1)