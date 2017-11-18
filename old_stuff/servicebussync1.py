import requests
import time
import random
import string
import json
import threading
import asyncio
from azure.servicebus import ServiceBusService, Message, Queue
from azure.storage.table import TableService, Entity


table_service = TableService(account_name='gregseon4e059a98c11c',\
    account_key='yE7Kuy0xVxUDR+wHGoWPjSpOhFO9WLd9b+t3+RI9C8tuBNbuLwEtWSQGERiO7LJRE1cFTGB0/TT4+CYGhtMfww==')
if not table_service.exists('Transactions'):
    table_service.create_table('Transactions')
bus_service = ServiceBusService(service_namespace='gregseon4e059a98c11c',\
    shared_access_key_name='RootManageSharedAccessKey',\
    shared_access_key_value='d8PrqA7to95t0wUFywAfhNDcbUwvh2sIpiHqvUdbPSQ=')
bus_service.create_queue('test4scaling')

products = ["Financial Trap", "Insurance", "Bitcoin", "Timeshares", "Food", "Clothes"]
def enqueue(start,stop):
    for x in range(start,stop):
        userid = "A" + str(random.randint(1,1000))
        sellerid = "S" + str(random.randint(1,1000))
        data = {"TransactionID":int(time.time()),"UserId":userid,'SellerID':sellerid,'ProductName':random.choice(products),"SalePrice":random.randint(1000,1000000),\
            'TransactionDate':time.strftime("%Y-%m-%d")}
        msg = Message(json.dumps(data))
        bus_service.send_queue_message('test4scaling', msg)

sttime = time.time()
threads = []
for i in range(1,51):
    start = 10 * (i - 1)
    end = 10 * i
    t = threading.Thread(target=enqueue, args=(start, end))
    # Sticks the thread in a list so that it remains accessible
    threads.append(t)
    t.start() 

for tr in threads:
    tr.join()
# if __name__ == '__main__':
#     enqueue()
print("Completed in {} seconds".format(time.time()-sttime))
# # while bus_service.get_queue('taskqueue').message_count > 0:
# #     msg = bus_service.receive_queue_message('taskqueue', peek_lock=True)
# #     print(msg.body)
# #     msg.delete()
