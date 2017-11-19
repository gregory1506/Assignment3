import socket
import threading
import time
from bottle import route, run, request
from azure.servicebus import ServiceBusService, Message, Queue
from config import queuename

hostname = socket.gethostname()
hostport = 9000
stime = time.time() # very close to when things get kicked off
status_msg = ''

def status():
    global stime
    global status_msg
    bus_service = ServiceBusService(service_namespace='gregseon4e059a98c11c',\
                  shared_access_key_name='RootManageSharedAccessKey',\
                  shared_access_key_value='4hUTgXrDAcs9S1fTOIjmyhDmFYFNduRSp+B04d0/Kmo=')
    bus_service.create_queue(queuename)
    while True:
        queuesize = bus_service.get_queue(queuename).message_count
        numseconds = time.time() - stime
        status_msg = "Queue size is {} after {} seconds".format(queuesize,numseconds)
        time.sleep(5)

def writebody():
    global status_msg
    body = '<html><head><title>work interface - build</title></head>'
    body += '<body><h2>worker interface on ' + hostname + '</h2><ul><h3>'
    body += '<br/>Current update: ' + status_msg
    body += '</h3></ul></body></html>'
    return body

@route('/')
def root():
    return writebody()

# @route('/do_work')
# def do_work():
#     return writebody()


# @route('/stop_work')
# def stop_work():
#     return writebody()
threading.Thread(target=status, args=()).start()
run(host=hostname, port=hostport)
