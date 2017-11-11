from azure.storage.queue import QueueService
import requests
import time
import random
import string
import json
import threading
products = ["Financial Trap","Insurance","Bitcoin","Timeshares","Food","Clothes"]
queue_service = QueueService(account_name='gjocloudassignment3',\
    account_key='7+WP5BOHFDDsBON6qqdqD8YdzQxUuP2jlcOIR/0b0Qvh/gduEVDI0YnoLYN82tZFq58H82+TdtDdsRJfOP+hjA==')
queue_service.create_queue('transactions')

def enqueue(a,b):
    for x in range(a,b):
        userid = "A" + str(random.randint(1,1000))
        sellerid = "S" + str(random.randint(1,1000))
        data = {"TransactionID":int(time.time()),"UserId":userid,'SellerID':sellerid,'ProductName':random.choice(products),"SalePrice":random.randint(1000,1000000),\
            'TransactionDate':time.strftime("%Y-%m-%d")}
        queue_service.put_message('transactions', json.dumps(data))
        # if x % 100 == 0:
        #     print(x)
sttime = time.time()
threads = []
for i in range(1,51):
    start = 100 * (i - 1)
    end = 100 * i
    t = threading.Thread(target=enqueue, args=(start, end))
    # Sticks the thread in a list so that it remains accessible
    threads.append(t)
    t.start()

for tr in threads:
    tr.join()

print("Completed in {} seconds".format(time.time()-sttime))



