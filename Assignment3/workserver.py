# workserver.py - simple HTTP server with a do_work / stop_work API
# GET /do_work activates a worker thread which uses CPU
# GET /stop_work signals worker thread to stop
import math
import socket
import threading
import time
import json
from bottle import route, run, request
from azure.servicebus import ServiceBusService, Message, Queue
from azure.storage.table import TableService, Entity

table_service = TableService(account_name='gregseon4e059a98c11c',\
    account_key='yE7Kuy0xVxUDR+wHGoWPjSpOhFO9WLd9b+t3+RI9C8tuBNbuLwEtWSQGERiO7LJRE1cFTGB0/TT4+CYGhtMfww==')
if not table_service.exists('Transactions'):
    table_service.create_table('Transactions')
bus_service = ServiceBusService(service_namespace='gregseon4e059a98c11c',\
    shared_access_key_name='RootManageSharedAccessKey',\
    shared_access_key_value='4hUTgXrDAcs9S1fTOIjmyhDmFYFNduRSp+B04d0/Kmo=')
bus_service.create_queue('taskqueue')


hostname = socket.gethostname()
hostport = 9000
sttime = time.time()
graph_pts = []
stmes = bus_service.get_queue('taskqueue').message_count

# thread which maximizes CPU usage while the keepWorking global is True
def workerthread():
    # outer loop to run while waiting
    while (True):
        # main loop to thrash the CPU
        while bus_service.get_queue('taskqueue').message_count > 0:
            msg = bus_service.receive_queue_message('taskqueue', peek_lock=True)
            data = json.loads(msg.body.decode('utf-8'))
            new_entity = Entity()
            new_entity.PartitionKey = data['TransactionID']
            new_entity.RowKey = data['UserId']
            new_entity.Sellerid = data['SellerID']
            new_entity.ProductName = data['ProductName']
            new_entity.SalePrice = data['SalePrice']
            new_entity.TransactionDate = data['TransactionDate']
            table_service.insert_or_replace_entity('Transactions',new_entity)
            msg.delete()

def writebody():
    global sttime
    global graph_pts
    body = '<html><head><title>work interface - build</title></head>'
    body += '<body><h2>worker interface on ' + hostname + '</h2><ul><h3>'

    if True:
        body += '<br/>worker thread is not running. <a href="./do_work">start work</a><br/>'
    else:
        body += '<br/>worker thread is running. <a href="./stop_work">stop work</a><br/>'
    current_count = stmes - bus_service.get_queue('taskqueue').message_count
    current_time = time.time() - sttime
    body += '<br/>usage:<br/><br/>/do_work = start worker thread<br/>/stop_work = stop worker thread<br/>'
    body += '<br/>Messages processed: ' + str(current_count)
    body += '<br/>Time from start : ' + str(current_time) + ' seconds<br/>'
    body += '</h3></ul></body></html>'
    graph_pts.append((current_count,current_time))
    return body

threads = []
for i in range(10):
    t = threading.Thread(target=workerthread, args=())
    # Sticks the thread in a list so that it remains accessible
    threads.append(t)
    t.start()

    #for tr in threads:
    #    tr.join()



@route('/')
def root():
    return writebody()

@route('/do_work')
def do_work():
    return writebody()


@route('/stop_work')
def stop_work():
    return writebody()

run(host=hostname, port=hostport)
