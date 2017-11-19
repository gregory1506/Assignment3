
import socket
import threading
import time
import json
from bottle import route, run, request
from azure.servicebus import ServiceBusService, Message, Queue
from read import readqueue
from config import queuename, tablename

hostname = socket.gethostname()
hostport = 9000

status_msg = ""

def worker():
    # outer loop to run while waiting
    global status_msg
    bus_service = ServiceBusService(service_namespace='gregseon4e059a98c11c',\
                  shared_access_key_name='RootManageSharedAccessKey',\
                  shared_access_key_value='4hUTgXrDAcs9S1fTOIjmyhDmFYFNduRSp+B04d0/Kmo=')
    bus_service.create_queue(queuename)
    stime = time.time()
    while (True):
        time.sleep(1)
        queuesize = bus_service.get_queue(queuename).message_count
        numseconds = time.time() - stime
        status_msg = "Queue size is {} after {} seconds".format(queuesize,numseconds)
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
            

def writebody():
    global sttime
    #global graph_pts
    body = '<html><head><title>work interface - build</title></head>'
    body += '<body><h2>worker interface on ' + hostname + '</h2><ul><h3>'
    body += '<br/>usage:<br/><br/>/do_work = start worker thread<br/>/stop_work = stop worker thread<br/>'
    body += '<br/>Current update: ' + status_msg
    body += '</h3></ul></body></html>'
    return body

worker()

@route('/')
def root():
    time.sleep(2)
    return writebody()

# @route('/do_work')
# def do_work():
#     return writebody()


# @route('/stop_work')
# def stop_work():
#     return writebody()

run(host=hostname, port=hostport)
