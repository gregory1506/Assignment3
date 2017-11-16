import time
import random
import json
import asyncio
from aiohttp import ClientSession
# from azure.servicebus import ServiceBusService, Message, Queue
# from azure.storage.table import TableService, Entity


# table_service = TableService(account_name='gregseon4e059a98c11c',\
#     account_key='yE7Kuy0xVxUDR+wHGoWPjSpOhFO9WLd9b+t3+RI9C8tuBNbuLwEtWSQGERiO7LJRE1cFTGB0/TT4+CYGhtMfww==')
# if not table_service.exists('Transactions'):
#     table_service.create_table('Transactions')
# bus_service = ServiceBusService(service_namespace='gregseon4e059a98c11c',\
#     shared_access_key_name='RootManageSharedAccessKey',\
#     shared_access_key_value='d8PrqA7to95t0wUFywAfhNDcbUwvh2sIpiHqvUdbPSQ=')
# bus_service.create_queue('test4scaling')

async def sendmsg(url,session):
    async with session.post() as response:
        return await response.read() 

async def run(r):
    tasks = []
    products = ["Financial Trap", "Insurance", "Bitcoin", "Timeshares", "Food", "Clothes"]
    # Fetch all responses within one Client session,
    # keep connection alive for all requests.
    async with ClientSession() as session:
        for i in range(r):
            userid = "A" + str(random.randint(1,1000))
            sellerid = "S" + str(random.randint(1,1000))
            data = {"TransactionID":int(time.time()),"UserId":userid,'SellerID':sellerid,'ProductName':random.choice(products),"SalePrice":random.randint(1000,1000000),\
                'TransactionDate':time.strftime("%Y-%m-%d")}
            msg = Message(json.dumps(data))
            task = asyncio.ensure_future(sendmsg(msg, session))
            tasks.append(task)

        responses = await asyncio.gather(*tasks)
        # you now have all response bodies in this variable
        print(responses)


sttime = time.time()
loop = asyncio.get_event_loop()
future = asyncio.ensure_future(run(100))
loop.run_until_complete(future)
print("Completed in {} seconds".format(time.time()-sttime))
# # while bus_service.get_queue('taskqueue').message_count > 0:
# #     msg = bus_service.receive_queue_message('taskqueue', peek_lock=True)
# #     print(msg.body)
# #     msg.delete()
