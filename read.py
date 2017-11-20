import time
import random
import json
import asyncio
from aiohttp import ClientSession
from sastoken import get_auth_token
from config import queuename, tablename, failqueue
from azure.storage.table import TableService
from azure.servicebus import ServiceBusService

# make Table if it doesn't exist
table_service = TableService(account_name='gregseon4e059a98c11c',\
    account_key='yE7Kuy0xVxUDR+wHGoWPjSpOhFO9WLd9b+t3+RI9C8tuBNbuLwEtWSQGERiO7LJRE1cFTGB0/TT4+CYGhtMfww==')
if not table_service.exists(tablename):
    table_service.create_table(tablename)

# make queues if they dont exist
bus_service = ServiceBusService(service_namespace='gregseon4e059a98c11c',\
    shared_access_key_name='RootManageSharedAccessKey',\
    shared_access_key_value='d8PrqA7to95t0wUFywAfhNDcbUwvh2sIpiHqvUdbPSQ=')
bus_service.create_queue(queuename)
bus_service.create_queue(failqueue)

#generate token for https comms
sas = get_auth_token("gregseon4e059a98c11c",queuename,"RootManageSharedAccessKey","d8PrqA7to95t0wUFywAfhNDcbUwvh2sIpiHqvUdbPSQ=")
sas2 = get_auth_token("gregseon4e059a98c11c",failqueue,"RootManageSharedAccessKey","d8PrqA7to95t0wUFywAfhNDcbUwvh2sIpiHqvUdbPSQ=")

async def tblwrite(msg,session):
    ''' Write message to table '''
    uri = "https://gregseon4e059a98c11c.table.core.windows.net/" + tablename + "?sv=2017-04-17&ss=bfqt&srt=sco&sp=rwdlacup&se=2017-11-30T08:49:46Z&st=2017-11-18T00:49:46Z&spr=https&sig=XL0n1GIAFRslWdTOZY8ivSqK7hQqW7SZXpLHCWrUSmw%3D"
    tid = str(msg["TransactionID"])
    suid = str(msg["UserId"]) + str(msg["SellerID"]) 
    data = json.dumps({"PartitionKey":tid,"RowKey": suid, "message":str(msg)})
    headers = {'Content-Type':'application/json;odata=nometadata','Content-Length':str(len(data)),'Prefer':'return-no-content'}
    async with session.post(uri,headers=headers,data=data) as response:
        if response.status == 409 or response.status == 204:
            pass  # this means it was either duplicate key pairs or inserted fine
        else:
            asyncio.sleep(5) # circuit breaker like approach that accepts that the message failed to be sent immediately and waits before resending same message.
            await tblwrite(msg,session)
        return response.status

async def sendfailure(data,session):
    ''' Write failure to second queue '''
    try:
        global sas2
        headers = {'Authorization':sas2["token"],'Content-Type':'Content-Type: application/vnd.microsoft.servicebus.json'}
        URL = "https://gregseon4e059a98c11c.servicebus.windows.net/"+failqueue+"/messages"
        async with session.post(URL, data=data, headers=headers) as response:
            if response.status != 201:
                asyncio.sleep(5) # sort of like a circuit breaker pattern. Wait 5 seconds and retry
                await sendfailure(data, session)
            return await response.read()
    except asyncio.TimeoutError:
        pass 

async def getmsg(session):
    ''' send message async '''
    global sas
    headers = {'Authorization':sas["token"], 'Content-Type': \
              'application/atom+xml;type=entry;charset=utf-8'}
    URL = "https://gregseon4e059a98c11c.servicebus.windows.net/"+queuename+"/messages/head"
    async with session.delete(URL, headers=headers) as response:
        if response.status not in (200,204):
            # add another read if https breaks downs for this read.
            # Message should still be in queue and unlocked for another competing consumer.
            await getmsg(session)
        elif response.status == 204: # means queue empty and nothing to write to table. return now
            return None
        else: # means message recieved
            msg = json.loads([x async for x in response.content][0].decode())
            if msg['failure'] == "yes":
                await sendfailure(msg,session) #write to failure queue is yes
            else:
                await tblwrite(msg, session)
        return await response.read()

async def boundgetmsg(sem, session):
    ''' async semaphore '''
    async with sem:
        await getmsg(session)

async def run(r):
    ''' kicks off the asynchronous generation of the post requests '''
    sem = asyncio.Semaphore(1000)
    tasks = []
    async with ClientSession() as session:
        for _ in range(r):
            task = asyncio.ensure_future(boundgetmsg(sem, session))
            tasks.append(task)
        responses = asyncio.gather(*tasks)
        await responses       

def readqueue(num_messages):
    N = num_messages
    LOOP = asyncio.get_event_loop()
    FUTURE = asyncio.ensure_future(run(N))
    LOOP.run_until_complete(FUTURE)
    return


