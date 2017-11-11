# workserver.py - simple HTTP server with a do_work / stop_work API
# GET /do_work activates a worker thread which uses CPU
# GET /stop_work signals worker thread to stop
import math
import socket
import threading
import time
import json
from bottle import route, run, request
#from azure.storage.queue import QueueService
from azure.storage.table import TableService, Entity
#queue_service = QueueService(account_name='gjocloudassignment3',\
#    account_key='7+WP5BOHFDDsBON6qqdqD8YdzQxUuP2jlcOIR/0b0Qvh/gduEVDI0YnoLYN82tZFq58H82+TdtDdsRJfOP+hjA==')
table_service = TableService(account_name='gjocloudassignment3',\
    account_key='7+WP5BOHFDDsBON6qqdqD8YdzQxUuP2jlcOIR/0b0Qvh/gduEVDI0YnoLYN82tZFq58H82+TdtDdsRJfOP+hjA==')
if not table_service.exists('Transactions'):
    table_service.create_table('Transactions')

hostname = socket.gethostname()
hostport = 9000
keepworking = False  # boolean to switch worker thread on or off


# thread which maximizes CPU usage while the keepWorking global is True
def workerthread():
    # outer loop to run while waiting
    while (True):
        # main loop to thrash the CPI
        while (keepworking == True):
            for x in range(1, 69):
                y = math.factorial(x)
        time.sleep(3)


# start the worker thread
worker_thread = threading.Thread(target=workerthread, args=())
worker_thread.start()


#def writebody():
#    body = '<html><head><title>work interface - build</title></head>'
#    body += '<body><h2>worker interface on ' + hostname + '</h2><ul><h3>'

#    if keepworking == false:
#        body += '<br/>worker thread is not running. <a href="./do_work">start work</a><br/>'
#    else:
#        body += '<br/>worker thread is running. <a href="./stop_work">stop work</a><br/>'

#    body += '<br/>usage:<br/><br/>/do_work = start worker thread<br/>/stop_work = stop worker thread<br/>'
#    body += '</h3></ul></body></html>'
#    return body


@route('/',method='POST')
def root():
    data = request.json
    new_entity = Entity()
    new_entity.PartitionKey = data['TransactionID']
    new_entity.RowKey = data['UserId']
    new_entity.Sellerid = data['Sellerid']
    new_entity.ProductName = entity['ProductName']
    new_entity.SalePrice = Entity['SalePrice']
    new_entity.TransactionDate = Entity['TransactionDate']
    mystorage.table_service.insert_or_replace_entity('Shots',new_entity)

#@route('/do_work')
#def do_work():
#    global keepworking
#    # start worker thread
#    keepworking = True
#    return writebody()


#@route('/stop_work')
#def stop_work():
#    global keepworking
#    # stop worker thread
#    keepworking = False
#    return writebody()


run(host=hostname, port=hostport)
