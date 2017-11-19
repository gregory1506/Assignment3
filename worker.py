import time
from azure.servicebus import ServiceBusService, Message, Queue
from read import readqueue
from config import queuename, tablename

def worker():
    # outer loop to run while waiting
    bus_service = ServiceBusService(service_namespace='gregseon4e059a98c11c',\
                  shared_access_key_name='RootManageSharedAccessKey',\
                  shared_access_key_value='4hUTgXrDAcs9S1fTOIjmyhDmFYFNduRSp+B04d0/Kmo=')
    bus_service.create_queue(queuename)
    while True:
        time.sleep(2)
        queuesize = bus_service.get_queue(queuename).message_count
        if queuesize >= 100000:
            readqueue(10000)
        elif queuesize >= 10000:
            readqueue(1000)
        elif queuesize >= 1000:
            readqueue(100)
        elif queuesize >= 100:
            readqueue(10)
        elif queuesize > 0:
            readqueue(5)
        else:
            time.sleep(30) # queue probably empty. wait 30 seconds before rechecking.

worker()
            

